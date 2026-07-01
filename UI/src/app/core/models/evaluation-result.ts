export interface SupportingEvidence {

    page: number;

    section: string;

    snippet: string;

}

export interface EvaluationResult {

    answer: string;

    confidence: number;

    justification: string;

    supporting_evidence: SupportingEvidence[];

}