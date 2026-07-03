from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from Backend.app.core.metrics import utc_now_iso
from Backend.app.models.claim_summary import ClaimSummary
from Backend.app.models.evaluation_result import EvaluationResult, RagasMetrics
from Backend.app.models.nurse_prompt import NursePrompt


@dataclass
class ClaimRecord:
    document_id: str
    namespace: str
    filename: str
    pdf_path: str
    created_at: str = field(default_factory=utc_now_iso)
    last_updated: str = field(default_factory=utc_now_iso)
    evaluations: list[EvaluationResult] = field(default_factory=list)

    @property
    def claim_id(self) -> str:
        return f"CLM-{self.document_id[:8].upper()}"


class ReviewStore:
    def __init__(self) -> None:
        self._claims: dict[str, ClaimRecord] = {}
        self._lock = Lock()

    def register_claim(
        self,
        *,
        document_id: str,
        namespace: str,
        filename: str,
        pdf_path: str,
    ) -> ClaimRecord:
        with self._lock:
            record = ClaimRecord(
                document_id=document_id,
                namespace=namespace,
                filename=filename,
                pdf_path=pdf_path,
            )
            self._claims[namespace] = record
            return record

    def add_evaluation(
        self,
        namespace: str,
        prompt: NursePrompt,
        result: EvaluationResult,
    ) -> None:
        with self._lock:
            record = self._claims.get(namespace)

            if record is None:
                record = ClaimRecord(
                    document_id=namespace,
                    namespace=namespace,
                    filename="Unknown medical record",
                    pdf_path="",
                )
                self._claims[namespace] = record

            enriched_result = result.model_copy(
                update={
                    "prompt_id": prompt.prompt_id,
                    "category": prompt.category,
                    "question": prompt.evaluation_prompt,
                    "guideline": prompt.guideline,
                    "decision_impact": result.decision_impact or prompt.decision_impact,
                }
            )

            record.evaluations = [
                item
                for item in record.evaluations
                if item.prompt_id != enriched_result.prompt_id
            ]
            record.evaluations.append(enriched_result)
            record.last_updated = utc_now_iso()

    def get_claim(self, namespace: str) -> ClaimRecord | None:
        with self._lock:
            record = self._claims.get(namespace)
            if record is None:
                return None
            # Return a shallow copy so callers cannot mutate the internal record.
            # evaluations list is copied; individual EvaluationResult objects are
            # Pydantic models and are effectively immutable via normal use.
            return ClaimRecord(
                document_id=record.document_id,
                namespace=record.namespace,
                filename=record.filename,
                pdf_path=record.pdf_path,
                created_at=record.created_at,
                last_updated=record.last_updated,
                evaluations=list(record.evaluations),
            )

    def list_dashboard_claims(self) -> list[dict[str, Any]]:
        with self._lock:
            # Deep-copy only what we need to avoid holding the lock during computation
            snapshots = [
                ClaimRecord(
                    document_id=r.document_id,
                    namespace=r.namespace,
                    filename=r.filename,
                    pdf_path=r.pdf_path,
                    created_at=r.created_at,
                    last_updated=r.last_updated,
                    evaluations=list(r.evaluations),
                )
                for r in self._claims.values()
            ]

        return [
            {
                "claim_id": record.claim_id,
                "namespace": record.namespace,
                "patient": "Uploaded Member",
                "diagnosis": self._diagnosis_label(record),
                "status": self._status_label(record),
                "verdict": self._claim_verdict(record),
                "confidence": self._average_confidence(record.evaluations),
                "reviewed_criteria": len(record.evaluations),
                "review_date": record.last_updated[:10],
                "filename": record.filename,
                "pdf_path": record.pdf_path,
            }
            for record in snapshots
        ]

    def build_summary(self, namespace: str) -> ClaimSummary | None:
        with self._lock:
            record = self._claims.get(namespace)
            if record is None:
                return None
            # Snapshot all mutable state under the lock before releasing it.
            evaluations = list(record.evaluations)
            claim_id = record.claim_id
            record_namespace = record.namespace
            filename = record.filename
            pdf_path = record.pdf_path
            created_at = record.created_at
            last_updated = record.last_updated

        valid_count = sum(1 for item in evaluations if item.verdict == "valid")
        insufficient_count = sum(
            1 for item in evaluations if item.verdict == "insufficient_evidence"
        )
        doubtful_count = len(evaluations) - valid_count - insufficient_count

        # Build a temporary record snapshot for the helper methods
        _snap = ClaimRecord(
            document_id=record_namespace,
            namespace=record_namespace,
            filename=filename,
            pdf_path=pdf_path,
            created_at=created_at,
            last_updated=last_updated,
            evaluations=evaluations,
        )
        verdict = self._claim_verdict(_snap)
        confidence = self._average_confidence(evaluations)
        ragas_metrics = self._average_ragas(evaluations)

        high_risk_findings = [
            item.final_summary
            for item in evaluations
            if item.verdict != "valid"
        ][:5]

        recommended_actions = self._recommended_actions(evaluations, verdict)

        return ClaimSummary(
            claim_id=claim_id,
            namespace=record_namespace,
            filename=filename,
            pdf_path=pdf_path,
            status=self._status_label(_snap),
            verdict=verdict,
            final_summary=self._final_summary(
                verdict=verdict,
                confidence=confidence,
                evaluations=evaluations,
            ),
            confidence=confidence,
            reviewed_criteria=len(evaluations),
            valid_criteria=valid_count,
            doubtful_criteria=doubtful_count,
            insufficient_evidence_criteria=insufficient_count,
            high_risk_findings=high_risk_findings,
            recommended_actions=recommended_actions,
            ragas_metrics=ragas_metrics,
            evaluation_results=evaluations,
            created_at=created_at,
            last_updated=last_updated,
        )

    def ragas_snapshot(self) -> dict[str, float]:
        with self._lock:
            evaluations = [
                evaluation
                for record in self._claims.values()
                for evaluation in record.evaluations
            ]

        metrics = self._average_ragas(evaluations)
        return metrics.model_dump() if metrics else {}

    def _diagnosis_label(self, record: ClaimRecord) -> str:
        if not record.evaluations:
            return "Awaiting review"

        categories = [
            item.category
            for item in record.evaluations
            if item.category
        ]
        return categories[0] if categories else "Clinical criteria"

    def _status_label(self, record: ClaimRecord) -> str:
        return "Completed" if record.evaluations else "Pending review"

    def _claim_verdict(self, record: ClaimRecord) -> str:
        if not record.evaluations:
            return "insufficient_evidence"

        if any(item.verdict != "valid" for item in record.evaluations):
            return "doubtful"

        return "valid"

    def _average_confidence(self, evaluations: list[EvaluationResult]) -> float:
        if not evaluations:
            return 0

        return round(
            sum(item.confidence for item in evaluations) / len(evaluations),
            1,
        )

    def _average_ragas(self, evaluations: list[EvaluationResult]) -> RagasMetrics | None:
        ragas_items = [
            item.ragas_metrics
            for item in evaluations
            if item.ragas_metrics
        ]

        if not ragas_items:
            return None

        fields = [
            "faithfulness",
            "answer_relevancy",
            "context_precision",
            "context_recall",
            "context_utilization",
        ]
        values: dict[str, float | None] = {}

        for field_name in fields:
            field_values = [
                value
                for item in ragas_items
                if (value := getattr(item, field_name)) is not None
            ]
            values[field_name] = (
                round(sum(field_values) / len(field_values), 3)
                if field_values
                else None
            )

        return RagasMetrics(**values)

    def _recommended_actions(
        self,
        evaluations: list[EvaluationResult],
        verdict: str,
    ) -> list[str]:
        actions: list[str] = []

        for item in evaluations:
            for action in item.follow_up_actions:
                if action and action not in actions:
                    actions.append(action)

        if actions:
            return actions[:6]

        if verdict == "valid":
            return [
                "Proceed with claim approval after standard human reviewer sign-off.",
                "Archive supporting evidence and reviewer trace for audit readiness.",
            ]

        return [
            "Route to clinical reviewer for manual adjudication.",
            "Request missing documentation for criteria marked doubtful or insufficient.",
        ]

    def _final_summary(
        self,
        *,
        verdict: str,
        confidence: float,
        evaluations: list[EvaluationResult],
    ) -> str:
        if not evaluations:
            return "No clinical criteria have been evaluated for this claim yet."

        if verdict == "valid":
            return (
                f"The claim currently appears valid across {len(evaluations)} reviewed "
                f"criteria with {confidence}% average confidence."
            )

        return (
            f"The claim is doubtful based on {len(evaluations)} reviewed criteria. "
            "At least one criterion lacks strong supporting evidence or requires manual review."
        )


review_store = ReviewStore()
