export interface SupportingEvidence {
  page: string;
  heading: string;
  evidence: string;
}

export interface EvaluationResult {
  answer: string;
  justification: string;
  supporting_evidence: SupportingEvidence[];
}