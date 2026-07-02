import { RagasMetrics } from './evaluation-result';

export interface LatencySummary {
  avg: number;
  p50: number;
  p95: number;
  max: number;
}

export interface TrafficMetrics {
  requests_total: number;
  errors_total: number;
  error_rate: number;
  status_counts: Record<string, number>;
  route_counts: Record<string, number>;
  latency_ms: LatencySummary;
}

export interface ReviewMetrics {
  evaluations_total: number;
  valid_total: number;
  doubtful_total: number;
  insufficient_evidence_total: number;
  average_confidence: number;
  average_retrieved_chunks: number;
  latency_ms: LatencySummary;
  model_counts: Record<string, number>;
}

export interface MetricsSnapshot {
  started_at: string;
  generated_at: string;
  traffic: TrafficMetrics;
  review: ReviewMetrics;
  ragas: Partial<RagasMetrics>;
}

export interface ObservabilitySnapshot {
  system: MetricsSnapshot;
  ragas: Partial<RagasMetrics>;
  claims: Array<{
    claim_id: string;
    namespace: string;
    patient: string;
    diagnosis: string;
    status: string;
    verdict: string;
    confidence: number;
    reviewed_criteria: number;
    review_date: string;
  }>;
}
