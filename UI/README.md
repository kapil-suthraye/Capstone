# UI — Angular 22 Reviewer Dashboard

Frontend for Medical AI Reviewer: upload medical-record PDFs, browse InterQual criteria, review AI verdicts side-by-side with the source PDF, and see claim summaries.

## Stack
Angular 22 (standalone components, SSR-ready), Angular Material + CDK, `ngx-extended-pdf-viewer`, `ngx-file-drop`.

## Run
```bash
npm install
npm start        # http://localhost:4200
```
Backend base URL is set in `src/environments/environment.ts` (default `http://localhost:8000/api`).
