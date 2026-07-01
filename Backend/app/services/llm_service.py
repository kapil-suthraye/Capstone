from __future__ import annotations

import json
import re
from time import perf_counter
from typing import Any
from uuid import uuid4

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from Backend.app.core.config import settings
from Backend.app.core.logging import logger
from Backend.app.core.metrics import metrics
from Backend.app.models.evaluation_result import (
    EvaluationResult,
    EvaluationTelemetry,
    SupportingEvidence,
)
from Backend.app.models.nurse_prompt import NursePrompt
from Backend.app.models.retrieved_chunk import RetrievedChunk
from Backend.app.services.ragas_service import RagasService
from Backend.app.services.vector_store import VectorStore


class LLMService:
    def __init__(self):
        self.vector = VectorStore()
        self.ragas = RagasService()
        self.primary_model = settings.OPENAI_MODEL
        self.fallback_model = settings.OPENAI_FALLBACK_MODEL
        self.llm = self._build_llm(self.primary_model)
        self.fallback_llm = (
            self._build_llm(self.fallback_model)
            if self.fallback_model and self.fallback_model != self.primary_model
            else None
        )

    PROMPT = ChatPromptTemplate.from_template(
        """
You are a senior medical claim AI reviewer. Use only the retrieved clinical
context to evaluate the review criterion. Do not infer facts that are not
supported by the evidence.

Return JSON only. The JSON must match this shape:
{{
  "answer": "short reviewer answer",
  "verdict": "valid | doubtful | insufficient_evidence",
  "confidence": 0-100,
  "final_summary": "one-paragraph claim-ready summary",
  "justification": "evidence-grounded rationale",
  "decision_impact": "approval, denial, manual review, or missing documentation impact",
  "follow_up_actions": ["action 1", "action 2"]
}}

Use "valid" only when the retrieved evidence clearly supports the criterion.
Use "doubtful" when evidence is mixed, partial, contradictory, or clinically
ambiguous. Use "insufficient_evidence" when the retrieved context does not
contain enough documentation to answer.

Review criterion:
{question}

Clinical context:
{context}
        """
    )

    def _build_llm(self, model: str) -> ChatOpenAI:
        return ChatOpenAI(
            model=model,
            api_key=settings.OPENAI_API_KEY,
            temperature=0,
        )

    def build_context(
        self,
        docs: list[RetrievedChunk],
    ) -> str:
        context = []

        for index, doc in enumerate(docs, start=1):
            context.append(
                f"""
[Chunk-{index}]
Chunk ID: {doc.chunk_id}
Score: {doc.score}
Heading: {doc.metadata.get("section_heading", "Unknown")}
Pages: {doc.metadata.get("page_start", "-")} - {doc.metadata.get("page_end", "-")}

{doc.text}
"""
            )

        return "\n\n".join(context)

    async def evaluate(
        self,
        namespace: str,
        prompt: NursePrompt,
    ) -> EvaluationResult:
        trace_id = str(uuid4())
        started = perf_counter()

        docs = await self.vector.retrieve(
            query=prompt.rag_search_keywords or prompt.evaluation_prompt,
            namespace=namespace,
            diagnosis_tag=None,
            top_k=settings.RETRIEVAL_TOP_K,
            rerank_top_n=settings.RERANK_TOP_N,
        )

        logger.bind(
            trace_id=trace_id,
            namespace=namespace,
            prompt_id=prompt.prompt_id,
            retrieved_chunks=len(docs),
        ).info("evaluation_context_retrieved")

        context = self.build_context(docs)
        messages = self.PROMPT.format_messages(
            question=prompt.evaluation_prompt,
            context=context,
        )

        response, model_used, fallback_used = await self._invoke_with_fallback(messages)
        data = self._parse_response(response.content)

        confidence = self._normalize_confidence(data.get("confidence"))
        verdict = self._normalize_verdict(
            data.get("verdict"),
            data.get("answer"),
            confidence,
        )
        latency_ms = round((perf_counter() - started) * 1000, 2)

        ragas_metrics = self.ragas.score(
            question=prompt.evaluation_prompt,
            answer=str(data.get("answer", "")),
            justification=str(data.get("justification", "")),
            contexts=docs,
            confidence=confidence,
        )

        telemetry = EvaluationTelemetry(
            trace_id=trace_id,
            model=model_used,
            fallback_model_used=fallback_used,
            latency_ms=latency_ms,
            retrieved_chunks=len(docs),
            evidence_count=min(len(docs), settings.RERANK_TOP_N),
            **self._usage(response),
        )

        result = EvaluationResult(
            prompt_id=prompt.prompt_id,
            category=prompt.category,
            question=prompt.evaluation_prompt,
            answer=str(data.get("answer", "Insufficient evidence")),
            verdict=verdict,
            confidence=confidence,
            final_summary=str(
                data.get("final_summary")
                or data.get("summary")
                or data.get("justification")
                or "The retrieved evidence was not sufficient for a confident determination."
            ),
            justification=str(
                data.get("justification")
                or "The model did not provide a detailed justification."
            ),
            supporting_evidence=self._supporting_evidence(docs),
            follow_up_actions=self._follow_up_actions(data.get("follow_up_actions"), verdict),
            guideline=prompt.guideline,
            decision_impact=str(data.get("decision_impact") or prompt.decision_impact or ""),
            ragas_metrics=ragas_metrics,
            telemetry=telemetry,
        )

        metrics.observe_evaluation(
            verdict=result.verdict,
            confidence=result.confidence,
            retrieved_chunks=len(docs),
            latency_ms=latency_ms,
            model=model_used,
            ragas_metrics=ragas_metrics.model_dump(),
        )

        logger.bind(
            trace_id=trace_id,
            namespace=namespace,
            prompt_id=prompt.prompt_id,
            verdict=result.verdict,
            confidence=result.confidence,
            latency_ms=latency_ms,
            model=model_used,
        ).info("evaluation_completed")

        return result

    async def evaluate_all(
        self,
        namespace: str,
        prompts: list[NursePrompt],
    ) -> list[EvaluationResult]:
        results = []

        for prompt in prompts:
            results.append(
                await self.evaluate(
                    namespace=namespace,
                    prompt=prompt,
                )
            )

        return results

    async def _invoke_with_fallback(self, messages):
        try:
            response = await self.llm.ainvoke(messages)
            return response, self.primary_model, None
        except Exception as exc:
            if not self.fallback_llm:
                raise

            logger.bind(
                primary_model=self.primary_model,
                fallback_model=self.fallback_model,
                error=str(exc),
            ).warning("primary_model_failed_using_fallback")

            response = await self.fallback_llm.ainvoke(messages)
            return response, self.fallback_model, self.fallback_model

    def _parse_response(self, content: str) -> dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, flags=re.DOTALL)

            if match:
                return json.loads(match.group(0))

            logger.bind(raw_response=content[:1000]).warning("llm_returned_non_json")
            return {
                "answer": "Insufficient evidence",
                "verdict": "insufficient_evidence",
                "confidence": 0,
                "final_summary": "The reviewer model did not return parseable JSON.",
                "justification": content,
                "follow_up_actions": ["Re-run review or route to manual clinical review."],
            }

    def _normalize_confidence(self, value: Any) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0

        if confidence <= 1:
            confidence *= 100

        return round(max(0, min(confidence, 100)), 1)

    def _normalize_verdict(
        self,
        verdict: Any,
        answer: Any,
        confidence: float,
    ) -> str:
        normalized = str(verdict or "").lower().replace(" ", "_")

        if normalized in {"valid", "doubtful", "insufficient_evidence"}:
            return normalized

        answer_text = str(answer or "").lower()

        if "insufficient" in answer_text or "not enough" in answer_text:
            return "insufficient_evidence"

        if "doubt" in answer_text or "manual" in answer_text or confidence < 70:
            return "doubtful"

        return "valid"

    def _supporting_evidence(
        self,
        docs: list[RetrievedChunk],
    ) -> list[SupportingEvidence]:
        evidence = []

        for doc in docs[: settings.RERANK_TOP_N]:
            page_start = doc.metadata.get("page_start", "-")
            page_end = doc.metadata.get("page_end", page_start)
            page = str(page_start)

            if page_end and page_end != page_start:
                page = f"{page_start} - {page_end}"

            evidence.append(
                SupportingEvidence(
                    page=page,
                    heading=str(doc.metadata.get("section_heading", "Unknown")),
                    score=doc.score,
                    evidence=doc.text[:500],
                    chunk_id=doc.chunk_id,
                )
            )

        return evidence

    def _follow_up_actions(
        self,
        actions: Any,
        verdict: str,
    ) -> list[str]:
        if isinstance(actions, list):
            normalized = [str(action) for action in actions if str(action).strip()]
            if normalized:
                return normalized[:6]

        if verdict == "valid":
            return ["Proceed with normal claim adjudication workflow."]

        return [
            "Route the claim to a clinical reviewer.",
            "Request missing documentation for unsupported criteria.",
        ]

    def _usage(self, response) -> dict[str, int | None]:
        usage = getattr(response, "usage_metadata", None) or {}
        response_metadata = getattr(response, "response_metadata", {}) or {}
        token_usage = response_metadata.get("token_usage", {}) or {}

        return {
            "prompt_tokens": usage.get("input_tokens") or token_usage.get("prompt_tokens"),
            "completion_tokens": usage.get("output_tokens") or token_usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens") or token_usage.get("total_tokens"),
        }
