export interface SupportingEvidence {

  page: number;

  section: string;

  snippet: string;

}

export interface EvaluationResult {

  answer: string;

  justification: string;

  confidence: number;

  supporting_evidence: SupportingEvidence[];

}