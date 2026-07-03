export interface NursePrompt {
  prompt_id: string;
  job_aid: string;
  category: string;
  evaluation_prompt: string;
  severity_level?: string | null;
  sheet_name?: string | null;
  document_source?: string | null;
  expected_finding?: string | null;
  red_flag?: string | null;
  guideline?: string | null;
  decision_impact?: string | null;
  rag_search_keywords?: string | null;
}
