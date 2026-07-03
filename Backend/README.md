# Backend — Medical AI Reviewer API

FastAPI service that powers ingestion (PDF → chunks → embeddings → Pinecone) and evaluation (retrieve → rerank → LLM verdict → RAGAS scoring) of medical-record claims against InterQual criteria.

## Layout
- `app/` — application code (routers, services, models, core config)
- `scripts/create_index.py` — one-time Pinecone index creation (3072-dim, cosine)
- `tests/` — pytest suite
- `requirements.txt` — Python dependencies

## Run
```bash
pip install -r Backend/requirements.txt
# create Backend/.env (see root README for variables)
python -m Backend.scripts.create_index   # one-time
uvicorn Backend.app.main:app --reload --port 8000
```
Interactive docs: http://localhost:8000/docs
