import { ClaimVerdict, EvaluationResult, RagasMetrics } from './evaluation-result';

export interface ClaimSummary {
  claim_id: string;
  namespace: string;
  filename?: string | null;
  pdf_path?: string | null;
  status: string;
  verdict: ClaimVerdict;
  final_summary: string;
  confidence: number;
  reviewed_criteria: number;
  valid_criteria: number;
  doubtful_criteria: number;
  insufficient_evidence_criteria: number;
  high_risk_findings: string[];
  recommended_actions: string[];
  ragas_metrics?: RagasMetrics | null;
  evaluation_results: EvaluationResult[];
  created_at: string;
  last_updated: string;
}
