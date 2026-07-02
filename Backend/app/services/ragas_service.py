from __future__ import annotations

from Backend.app.models.evaluation_result import RagasMetrics
from Backend.app.models.retrieved_chunk import RetrievedChunk


class RagasService:
    """RAGAS-compatible metric facade.

    The production RAGAS package can be connected here when curated ground truth
    is available. Until then, these deterministic proxy scores keep observability
    stable and make low-evidence answers visible to reviewers.
    """

    def score(
        self,
        *,
        question: str,
        answer: str,
        justification: str,
        contexts: list[RetrievedChunk],
        confidence: float,
    ) -> RagasMetrics:
        if not contexts:
            return RagasMetrics(
                faithfulness=0,
                answer_relevancy=0,
                context_precision=0,
                context_recall=0,
                context_utilization=0,
                notes="No retrieved context was available for RAGAS scoring.",
            )

        question_terms = self._terms(question)
        answer_terms = self._terms(f"{answer} {justification}")
        context_terms = self._terms(" ".join(item.text for item in contexts))

        overlap_with_context = self._overlap(answer_terms, context_terms)
        overlap_with_question = self._overlap(answer_terms, question_terms)
        context_question_overlap = self._overlap(context_terms, question_terms)
        utilization = min(1, len(contexts) / 12)
        confidence_factor = max(0, min(confidence / 100, 1))

        return RagasMetrics(
            faithfulness=round((overlap_with_context * 0.7) + (confidence_factor * 0.3), 3),
            answer_relevancy=round(overlap_with_question, 3),
            context_precision=round(context_question_overlap, 3),
            context_recall=round(min(1, context_question_overlap + utilization * 0.25), 3),
            context_utilization=round(utilization, 3),
        )

    def _terms(self, text: str) -> set[str]:
        return {
            token.strip(".,:;()[]{}!?").lower()
            for token in text.split()
            if len(token.strip(".,:;()[]{}!?")) > 3
        }

    def _overlap(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0

        return len(left & right) / len(left)
