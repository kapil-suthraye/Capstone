export interface UploadResponse {
  document_id: string;
  namespace: string;
  filename: string;
  pdf_path: string;
  chunks: number;
  message: string;
  detected_diagnosis?: string | null;
}
