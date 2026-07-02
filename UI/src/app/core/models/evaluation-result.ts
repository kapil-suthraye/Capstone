export interface SupportingEvidence {
  page: string;
  heading: string;
  evidence: string;
  score?: number | null;
  chunk_id?: string | null;
}

export type ClaimVerdict = 'valid' | 'doubtful' | 'insufficient_evidence';

export interface RagasMetrics {
  faithfulness?: number | null;
  answer_relevancy?: number | null;
  context_precision?: number | null;
  context_recall?: number | null;
  context_utilization?: number | null;
  notes?: string;
}

export interface EvaluationTelemetry {
  trace_id: string;
  model: string;
  fallback_model_used?: string | null;
  latency_ms: number;
  retrieved_chunks: number;
  evidence_count: number;
  prompt_tokens?: number | null;
  completion_tokens?: number | null;
  total_tokens?: number | null;
}

export interface EvaluationResult {
  prompt_id?: string | null;
  category?: string | null;
  question?: string | null;
  answer: string;
  verdict: ClaimVerdict;
  confidence: number;
  final_summary: string;
  justification: string;
  supporting_evidence: SupportingEvidence[];
  follow_up_actions: string[];
  guideline?: string | null;
  decision_impact?: string | null;
  ragas_metrics?: RagasMetrics | null;
  telemetry?: EvaluationTelemetry | null;
}
