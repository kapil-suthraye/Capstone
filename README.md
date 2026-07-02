<div align="center">

# 🩺 Medical AI Reviewer

### An agentic, evidence-grounded RAG system that reviews medical claims against InterQual clinical criteria — and shows its work.

</div>

---

## 📖 Overview

**Medical AI Reviewer** ingests raw medical-record PDFs, indexes them into a vector database, and evaluates them against a curated library of **nurse-authored InterQual review criteria**. For every criterion it returns a verdict (`valid` / `doubtful` / `insufficient_evidence`), a confidence score, an evidence-grounded justification with page citations, and recommended follow-up actions — all surfaced through an Angular reviewer dashboard.

The system is built for the realities of clinical claim review: **traceability, auditability, and observability are first-class citizens**. Every evaluation carries a trace ID, token accounting, latency telemetry, and RAGAS-style retrieval-quality metrics.

> ⚠️ **Disclaimer:** This is a capstone/research project. It is a decision-support prototype, not a certified clinical or claims-adjudication tool, and always routes final sign-off to a human reviewer.

---

## ✨ Key Features

| | Feature | What it does |
|---|---|---|
| 📄 | **Structure-aware PDF parsing** | Extracts text with font, coordinate, and bold heuristics to reconstruct clinical document structure (headings, sections, tables). |
| ✂️ | **Clinical-aware chunking** | Token-budgeted, section-scoped chunker that tags diagnoses, medications, and lab values, and scores each chunk by clinical importance. |
| 🔍 | **Two-stage retrieval** | Dense similarity search over Pinecone (`top_k=50`) followed by hosted **BGE reranking** (`top_n=12`) for precision. |
| 🧠 | **Grounded LLM evaluation** | GPT-5.5 reviewer with an automatic fallback model, strict JSON output, and verdict/confidence normalization. |
| 📊 | **RAGAS-style scoring** | Deterministic faithfulness, answer-relevancy, context-precision/recall, and utilization proxies for every answer. |
| 🗂️ | **Nurse prompt library** | InterQual review criteria loaded from an Excel job-aid workbook and exposed via the API. |
| 📈 | **Full observability** | Request + evaluation metrics (latency p50/p95, error rates, token usage, verdict distribution) at `/api/observability`. |
| 🖥️ | **Reviewer dashboard** | Angular 22 UI for upload, side-by-side PDF review, per-claim summaries, and evidence cards. |

---

## 🏗️ Architecture

```
                        ┌──────────────────────────────────────────┐
                        │            Angular 22 Frontend             │
                        │  Upload · Dashboard · Review · Summary     │
                        └────────────────────┬───────────────────────┘
                                             │  REST (/api)
                        ┌────────────────────▼───────────────────────┐
                        │              FastAPI Backend                 │
                        │  observability middleware · request tracing  │
                        └───┬───────────────┬───────────────┬─────────┘
                            │               │               │
            ┌───────────────▼──┐   ┌────────▼─────────┐   ┌─▼──────────────┐
            │  Ingestion        │   │  Evaluation      │   │  Review Store  │
            │  PDF ▸ Parse ▸    │   │  Retrieve ▸      │   │  claims,       │
            │  Chunk ▸ Embed ▸  │   │  Rerank ▸ LLM ▸  │   │  summaries,    │
            │  Upsert           │   │  RAGAS           │   │  dashboard     │
            └────────┬──────────┘   └────────┬─────────┘   └────────────────┘
                     │                       │
              ┌──────▼──────┐         ┌───────▼────────┐
              │  Pinecone   │◀────────│  OpenAI        │
              │  Vector DB  │  embed  │  Embeddings +  │
              │ (namespaces)│  rerank │  Chat models   │
              └─────────────┘         └────────────────┘
```

**Ingestion pipeline:** `PDF → PDFParser → Chunker → EmbeddingService → VectorStore (Pinecone)`

**Evaluation pipeline:** `NursePrompt → VectorStore.retrieve → LLMService → RagasService → ReviewStore`

Each uploaded document gets a unique `document_id` that doubles as its **Pinecone namespace**, keeping every claim's evidence fully isolated.

---

## 🧰 Tech Stack

**Backend**
- **FastAPI** + **Uvicorn** — async API layer with request-level observability middleware
- **LangChain / LangGraph** — LLM orchestration and prompt templating
- **OpenAI** — `gpt-5.5` reviewer (with `gpt-5.4-mini` fallback) and `text-embedding-3-large` embeddings
- **Pinecone** — serverless vector store (3072-dim, cosine) with hosted `bge-reranker-v2-m3` reranking
- **pypdf** — structure-aware PDF extraction · **tiktoken** — token budgeting
- **openpyxl** — nurse prompt / ground-truth workbook loading
- **Pydantic v2** — typed models and settings · **Loguru** — structured logging ·

**Frontend**
- **Angular 22** (standalone components, SSR-ready) + **Angular Material** + **CDK**
- **ngx-extended-pdf-viewer** — in-browser PDF review · **ngx-file-drop** — upload UX

---

## 📁 Project Structure

```
Capstone-feature/
├── Backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routers: upload, evaluate, summary,
│   │   │                        #   dashboard, prompts, health, observability
│   │   ├── core/                # config, constants, logging, metrics
│   │   ├── db/                  # in-memory review store (claims + summaries)
│   │   ├── models/              # Pydantic models (chunks, prompts, results…)
│   │   ├── orchestrator/        # LangGraph workflow scaffolding
│   │   ├── services/            # parser, chunker, embeddings, vector store,
│   │   │                        #   retriever, LLM, RAGAS, nurse prompts
│   │   ├── utils/               # heading detection, token counting
│   │   └── main.py              # FastAPI app + middleware wiring
│   ├── scripts/create_index.py  # one-time Pinecone index creation
│   ├── tests/                   # pytest suite
│   └── requirements.txt
├── UI/                          # Angular 22 reviewer dashboard
│   └── src/app/
│       ├── core/                # API services + typed models
│       ├── features/            # dashboard, upload, review, claim-summary
│       ├── layout/              # header, sidebar, dashboard layout
│       └── shared/components/   # stat cards, evidence cards, PDF viewer…
├── data/
│   ├── jobaids/                 # nurse_prompts_interqual.xlsx (review criteria)
│   ├── gt/                      # ground_truth_all_cases.xlsx (evaluation set)
│   └── medical_records/         # sample raw medical-record PDFs
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm 11+**
- A **Pinecone** account + API key
- An **OpenAI** API key

### 1. Backend setup

```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r Backend/requirements.txt
```

Create a `.env` file in the `Backend/` directory:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.5
OPENAI_FALLBACK_MODEL=gpt-5.4-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

PINECONE_API_KEY=...
PINECONE_INDEX_NAME=medical-ai-reviewer
PINECONE_ENVIRONMENT=us-east-1

CORS_ORIGINS=http://localhost:4200
RETRIEVAL_TOP_K=50
RERANK_TOP_N=12

# Optional LangSmith tracing
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=Medical-AI-Reviewer
```

Create the Pinecone index (one-time), then start the API:

```bash
python -m Backend.scripts.create_index      # creates a 3072-dim cosine index
uvicorn Backend.app.main:app --reload --port 8000
```

The API is now live at **http://localhost:8000** — interactive docs at **http://localhost:8000/docs**.

### 2. Frontend setup

```bash
cd UI
npm install
npm start          # ng serve
```

Open **http://localhost:4200**. The UI talks to the backend at `http://localhost:8000/api` (configured in `src/environments/environment.ts`).

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/health` | Service health + version. |
| `POST` | `/api/upload` | Upload a medical-record PDF → parses, chunks, embeds, and upserts to Pinecone. Returns `document_id`, `namespace`, and chunk count. |
| `GET`  | `/api/prompts` | List all InterQual nurse review prompts. |
| `POST` | `/api/evaluate` | Evaluate one prompt against a claim. Body: `{ "namespace": "...", "prompt_id": "..." }`. |
| `GET`  | `/api/claims/{namespace}/summary` | Aggregated claim summary: verdict, confidence, high-risk findings, recommended actions. |
| `GET`  | `/api/dashboard` | All reviewed claims for the dashboard grid. |
| `GET`  | `/api/metrics` | System + review metrics snapshot. |
| `GET`  | `/api/observability` | Combined system, RAGAS, and claim observability. |

<details>
<summary><b>Example: end-to-end review flow</b></summary>

```bash
# 1. Upload a record
curl -F "file=@data/medical_records/medical_records_raw_v1.pdf" \
     http://localhost:8000/api/upload
# → { "document_id": "…", "namespace": "…", "chunks": 42, ... }

# 2. Discover available criteria
curl http://localhost:8000/api/prompts

# 3. Evaluate a criterion against the claim
curl -X POST http://localhost:8000/api/evaluate \
     -H "Content-Type: application/json" \
     -d '{"namespace":"<namespace>","prompt_id":"<prompt_id>"}'

# 4. Pull the aggregated claim summary
curl http://localhost:8000/api/claims/<namespace>/summary
```

</details>

---

## 🧭 How It Works (in depth)

1. **Parse.** `PDFParser` walks each page with a `pypdf` visitor, capturing text plus font size, font name, coordinates, and a bold heuristic, then reassembles fragments into top-to-bottom ordered lines.
2. **Chunk.** `Chunker` detects headings and tables, builds section-scoped paragraphs, splits sentences, and packs them into ~700-token chunks with 75-token overlap. Each chunk is enriched with a diagnosis tag, detected medications, lab values, a section priority, and a clinical-importance score.
3. **Embed & store.** `EmbeddingService` batches chunks through `text-embedding-3-large`; `VectorStore` upserts them into a per-claim Pinecone namespace with retry/backoff.
4. **Retrieve.** For a given prompt, the system runs dense similarity search then hosted BGE reranking to surface the most relevant evidence.
5. **Evaluate.** `LLMService` feeds the reranked context into a strict-JSON reviewer prompt, normalizes the verdict and confidence, and attaches supporting evidence with page citations and follow-up actions.
6. **Score & record.** `RagasService` computes retrieval-quality proxies, `MetricsRegistry` records telemetry, and `ReviewStore` aggregates everything into dashboard and summary views.

---

## 🗺️ Future Enhancements

- [ ] Wire the **production RAGAS** package against the `data/gt` ground-truth set
- [ ] Ship the **Observability** frontend route (scaffolded, currently disabled)

---

<div align="center">

**Built as a capstone project — engineered for traceable, auditable clinical claim review.**

</div>
