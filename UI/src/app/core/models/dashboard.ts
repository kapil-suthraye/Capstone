export interface DashboardClaim {
  claim_id: string;
  namespace: string;
  patient: string;
  diagnosis: string;
  status: string;
  verdict: string;
  confidence: number;
  reviewed_criteria: number;
  review_date: string;
  filename?: string;
  pdf_path?: string;
  detected_diagnosis?: string | null;
}
