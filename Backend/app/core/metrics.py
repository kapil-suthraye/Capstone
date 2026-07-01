from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from statistics import mean
from threading import Lock
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MetricsRegistry:
    def __init__(self) -> None:
        self.started_at = utc_now_iso()
        self._lock = Lock()
        self._request_latencies: deque[float] = deque(maxlen=1000)
        self._evaluation_latencies: deque[float] = deque(maxlen=1000)
        self._retrieved_chunks: deque[int] = deque(maxlen=1000)
        self._confidence_scores: deque[float] = deque(maxlen=1000)
        self._ragas_scores: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=1000))
        self.request_count = 0
        self.error_count = 0
        self.evaluations_total = 0
        self.valid_claims_total = 0
        self.doubtful_claims_total = 0
        self.insufficient_evidence_total = 0
        self.status_counts: dict[str, int] = defaultdict(int)
        self.route_counts: dict[str, int] = defaultdict(int)
        self.model_counts: dict[str, int] = defaultdict(int)

    def observe_request(
        self,
        method: str,
        path: str,
        status_code: int,
        latency_ms: float,
    ) -> None:
        with self._lock:
            self.request_count += 1
            self.status_counts[str(status_code)] += 1
            self.route_counts[f"{method} {path}"] += 1
            self._request_latencies.append(latency_ms)
            if status_code >= 500:
                self.error_count += 1

    def observe_evaluation(
        self,
        *,
        verdict: str,
        confidence: float,
        retrieved_chunks: int,
        latency_ms: float,
        model: str,
        ragas_metrics: dict[str, Any] | None = None,
    ) -> None:
        with self._lock:
            self.evaluations_total += 1
            self._confidence_scores.append(confidence)
            self._retrieved_chunks.append(retrieved_chunks)
            self._evaluation_latencies.append(latency_ms)
            self.model_counts[model] += 1

            if verdict == "valid":
                self.valid_claims_total += 1
            elif verdict == "insufficient_evidence":
                self.insufficient_evidence_total += 1
            else:
                self.doubtful_claims_total += 1

            for name, value in (ragas_metrics or {}).items():
                if isinstance(value, int | float):
                    self._ragas_scores[name].append(float(value))

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            request_latencies = list(self._request_latencies)
            evaluation_latencies = list(self._evaluation_latencies)
            retrieved_chunks = list(self._retrieved_chunks)
            confidence_scores = list(self._confidence_scores)

            return {
                "started_at": self.started_at,
                "generated_at": utc_now_iso(),
                "traffic": {
                    "requests_total": self.request_count,
                    "errors_total": self.error_count,
                    "error_rate": self._safe_ratio(self.error_count, self.request_count),
                    "status_counts": dict(self.status_counts),
                    "route_counts": dict(self.route_counts),
                    "latency_ms": self._latency_summary(request_latencies),
                },
                "review": {
                    "evaluations_total": self.evaluations_total,
                    "valid_total": self.valid_claims_total,
                    "doubtful_total": self.doubtful_claims_total,
                    "insufficient_evidence_total": self.insufficient_evidence_total,
                    "average_confidence": self._avg(confidence_scores),
                    "average_retrieved_chunks": self._avg(retrieved_chunks),
                    "latency_ms": self._latency_summary(evaluation_latencies),
                    "model_counts": dict(self.model_counts),
                },
                "ragas": {
                    name: self._avg(list(values))
                    for name, values in self._ragas_scores.items()
                },
            }

    def _latency_summary(self, values: list[float]) -> dict[str, float]:
        return {
            "avg": self._avg(values),
            "p50": self._percentile(values, 50),
            "p95": self._percentile(values, 95),
            "max": max(values) if values else 0,
        }

    def _avg(self, values: list[int] | list[float]) -> float:
        return round(float(mean(values)), 2) if values else 0

    def _percentile(self, values: list[float], percentile: int) -> float:
        if not values:
            return 0

        ordered = sorted(values)
        index = min(
            len(ordered) - 1,
            max(0, round((percentile / 100) * (len(ordered) - 1))),
        )
        return round(float(ordered[index]), 2)

    def _safe_ratio(self, numerator: int, denominator: int) -> float:
        return round(numerator / denominator, 4) if denominator else 0


metrics = MetricsRegistry()