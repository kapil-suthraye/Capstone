# data/ — Reference & Sample Data

- `jobaids/nurse_prompts_interqual.xlsx` — nurse-authored InterQual review criteria; loaded by the backend and served at `GET /api/prompts`
- `gt/ground_truth_all_cases.xlsx` — labeled evaluation set for measuring verdict quality (planned production-RAGAS wiring)
- `medical_records/` — sample raw medical-record PDFs (v1–v3) for demos and testing

⚠️ Synthetic/sample data only — never commit real patient records (PHI) to this repository.
