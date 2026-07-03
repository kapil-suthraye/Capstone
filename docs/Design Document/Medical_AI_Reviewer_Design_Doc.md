# Medical AI Reviewer — Design Document

### An Agentic RAG Architecture for Post-Payment Claim Review Support

**Prepared by:** Shirisha Dhannini & Kapil Suthraye

**Programme:** EY Generative AI Training

**Organisation:** Ernst & Young (EY) | Hyderabad, India

---

## Table of Contents

1. Project Overview & Problem Statement
2. Market Research & Opportunity
3. Proposed Solution
4. Project Type Classification
5. High-Level Architecture
6. Tech Stack & Technology Choices
7. Agent Design
8. Data Sources & Schema
9. Guardrails & Safety
10. Observability & Monitoring
11. Evaluation Metrics
12. Success Metrics

---

## 1. Project Overview & Problem Statement

Insurance companies conduct post-payment claim reviews to verify that providers billed correctly and that medical records support the payments already made. This process is performed manually by clinical nurse reviewers, who must navigate lengthy patient records — often exceeding 1,000 pages — to locate relevant clinical evidence and assess whether billed services are adequately documented and justified.

**Key Challenges:**
- Medical records frequently exceed 1,000 pages, making manual review slow and cognitively demanding.
- A nurse reviewer can process only 4–5 claims per day, while insurers may receive thousands of claims for review daily.
- The process relies entirely on trained clinical professionals, making it expensive and difficult to scale.
- Delayed reviews slow down recovery actions and increase the risk of uncollected overpayments.
- Manual review of large, unstructured records leads to inconsistent outcomes across different reviewers.

## 2. Market Research & Opportunity

The healthcare claims management and review market is experiencing significant growth, driven by rising claim volumes, increasing complexity of medical coding (ICD-10/CPT), and growing pressure on payers to reduce overpayment leakage. AI-assisted review tools represent one of the highest-ROI applications of Generative AI in healthcare payer operations.

| Metric | Insight |
|---|---|
| Daily claim review demand | Thousands of claims per insurer per day vs. 4–5 claims per nurse |
| Average medical record length | Often exceeds 1,000 pages per patient episode |
| Cost driver | High dependence on trained clinical reviewers; expensive to scale |
| Recovery opportunity | AI first-pass reduces missed discrepancy risk and speeds recovery actions |
| Competitive landscape | Emerging space — RAG + clinical NLP solutions beginning to appear in payer tech |
| Regulatory context | Human-in-the-loop mandatory; AI cannot auto-deny or auto-recoup payments |

**Opportunity Summary:**
- Reduce per-claim review cost by augmenting nurses with AI-prepared evidence packages.
- Scale review capacity without proportional headcount increases.
- Improve consistency and auditability of review decisions.
- Enable focus on high-complexity cases by automating initial evidence extraction.

## 3. Proposed Solution

Medical AI Reviewer is an **agentic, evidence-grounded Retrieval-Augmented Generation (RAG) system** designed to support post-payment claim review. It ingests raw medical-record PDFs, indexes them into a Pinecone vector database, and evaluates them against a curated library of **nurse-authored InterQual review criteria**, presenting evidence-cited verdicts and summaries to the nurse reviewer.

The system shifts the nurse's role from reading everything manually to reviewing AI-prepared evidence and making the final clinical and compliance decision.

**Core Capabilities (implemented):**
- Ingest and process large medical-record PDFs with structure-aware parsing (font, coordinate, and bold heuristics reconstruct headings, sections, and tables).
- Chunk records into clinical-aware, section-scoped segments (~700 tokens, 75-token overlap) tagged with diagnoses, medications, lab values, and a clinical-importance score.
- Embed (OpenAI `text-embedding-3-large`, 3072-dim) and index chunks in Pinecone, one **namespace per document** for full claim isolation.
- Retrieve the most relevant passages per InterQual criterion via **two-stage retrieval**: dense similarity search (top-50) followed by hosted BGE reranking (top-12).
- Evaluate each criterion with a **grounded GPT-5.5 reviewer** (strict-JSON output, automatic fallback to gpt-5.4-mini), returning a normalized verdict (`valid` / `doubtful` / `insufficient_evidence`), confidence, page-cited justification, and recommended follow-up actions.
- Score every answer with RAGAS-style metrics (faithfulness, answer relevancy, context precision/recall, utilization).
- Aggregate per-criterion results into claim-level summaries with high-risk findings, surfaced through an Angular reviewer dashboard.

**Planned extensions:** OCR for scanned records, interactive reviewer Q&A, and a reviewer feedback loop.

## 4. Project Type Classification

**Primary Type:** Medical Document Summarizer + Clinical Evidence Recommender

- **Summarization:** Converts lengthy, unstructured medical records into concise, structured reviewer-friendly outputs with per-criterion verdicts.
- **Evidence Recommendation:** Surfaces the most relevant clinical passages with page citations and flags discrepancies to help nurses validate claims faster.

This classification places the system in the category of **AI-augmented decision support — not autonomous decision-making**. The AI prepares, organises and highlights; the nurse decides.

## 5. High-Level Architecture

The system is built as an **agentic RAG pipeline coordinated by the FastAPI backend** (with LangGraph workflow scaffolding for future multi-agent expansion). Medical records flow through an **Ingestion agent** (parse → chunk → embed → upsert) into a per-document Pinecone namespace. On evaluation, a **Retrieval & Rerank stage** fetches semantically relevant evidence, the **LLM Evaluation agent** performs grounded reasoning and verdict generation, and the **RAGAS + Summary stage** scores retrieval quality and aggregates results into the ReviewStore. The Angular dashboard surfaces everything to the human-in-the-loop layer. The MetricsRegistry (with optional LangSmith) provides end-to-end observability.

*Figure 1: Medical AI Reviewer — Agentic RAG Architecture (see `docs/High Level Architecture/Medical AI Reviewer - Agentic RAG Architecture.drawio`)*

**Component Summary:**

| Component | Role |
|---|---|
| User / UI (Angular 22) | Nurse Reviewer Dashboard — Upload, Claim Detail, Side-by-side Evidence View, Claim Summary |
| Orchestrator (FastAPI + LangGraph scaffolding) | Workflow coordination, retry logic, LLM fallback, request tracing, guardrails (strict-JSON, verdict normalization) |
| Ingestion Agent | Structure-aware PDF parsing, clinical chunking, embedding, namespace-scoped Pinecone upsert |
| Retrieval & Rerank | Dense semantic search (top-50) + hosted `bge-reranker-v2-m3` (top-12) |
| LLM Evaluation Agent | Grounded clinical reasoning, verdict + confidence + page citations + follow-up actions |
| RAGAS Scoring + Summary | Retrieval-quality scoring; claim-level aggregation for dashboard and summary views |
| Vector DB (Pinecone serverless) | Stores chunk embeddings (3072-dim, cosine); namespace per document; hosted reranking; citation lookup |
| Review Store (in-memory) | Evaluation results, claim summaries, dashboard views, history |
| Human-in-the-Loop | Nurse approves, rejects, or escalates; final decision authority |
| Observability (MetricsRegistry + Loguru, optional LangSmith) | Traces, token accounting, latency p50/p95, error rates, verdict distribution |
| OpenAI Models | GPT-5.5 reasoning/verdicts (fallback gpt-5.4-mini); `text-embedding-3-large` embeddings |
| External Data Sources | Medical-record PDFs, InterQual nurse prompts (Excel), ground-truth workbook |

## 6. Tech Stack & Technology Choices

Each technology in the stack was selected for a specific reason. The table below documents the implemented choice, its purpose, and its trade-offs.

| Layer | Technology | Purpose | Pros | Cons / Trade-offs |
|---|---|---|---|---|
| Frontend | Angular 22 + Material | Reviewer dashboard: upload, review, summaries | Production-grade SPA; typed API services; rich components (PDF viewer, drag-drop) | Heavier than Streamlit for prototyping; requires frontend expertise |
| Backend | Python + FastAPI | Core API and AI pipeline logic | Async, Pydantic v2 validation, auto OpenAPI docs, middleware hooks for observability | Async patterns add complexity; GIL limits CPU parallelism |
| Doc Parsing | pypdf (structure-aware) + tiktoken | Extract text with font/coordinate/bold structure; token budgeting | Preserves clinical document structure that drives chunk quality; no external service | No OCR — scanned records unsupported (planned); custom visitor code to maintain |
| Embeddings | OpenAI `text-embedding-3-large` | Convert chunks into 3072-dim vectors | High retrieval quality; no local inference infra; batched API | API cost and dependency; re-embedding needed on model change |
| Vector Store | Pinecone (serverless) | Store and retrieve chunk embeddings | Managed persistence; **namespaces for claim isolation**; hosted BGE reranking; metadata filtering | Vendor dependency and cost vs. local FAISS |
| Reranking | Hosted `bge-reranker-v2-m3` | Precision re-ordering of retrieved chunks | Cross-encoder accuracy without hosting a model | Extra latency and cost per query |
| AI / LLM | GPT-5.5 (fallback gpt-5.4-mini) | Evidence analysis, verdicts, summaries | Strong grounded reasoning; reliable strict-JSON; automatic cheaper fallback | Cost and latency; API dependency |
| RAG Framework | LangChain / LangGraph | Prompt templating and workflow orchestration | Mature ecosystem; LangGraph enables multi-agent evolution | Abstraction overhead; rapid API changes |
| Storage | In-memory ReviewStore | Store evaluation results, summaries, history | Zero ops for prototype; single seam to swap for a DB | No persistence across restarts; not multi-instance safe |
| Observability | MetricsRegistry + Loguru (+ optional LangSmith) | Trace requests, evaluations, tokens, latency | Local, always-on telemetry; `/api/metrics` + `/api/observability`; structured logs | Custom registry to maintain; LangSmith optional adds cost/data egress |
| Evaluation | RAGAS-style deterministic proxies | Score retrieval and answer quality per response | Zero extra LLM cost; continuous signal on every answer | Proxies are less faithful than full RAGAS; ground-truth wiring planned |
| Deployment | Docker + docker-compose | Containerised backend and UI | Reproducible environments; simple orchestration | Not a managed/scaled cloud deployment |

## 7. Agent Design

**Orchestrator (FastAPI + LangGraph scaffolding)**
Central controller of the pipeline.
- Receives upload and evaluation requests from the UI layer via REST routers.
- Coordinates the sequence of service calls per task (ingestion vs. evaluation).
- Manages per-request state, trace IDs, and telemetry via observability middleware.
- Handles retry logic (vector upserts) and failure recovery (automatic LLM fallback model).
- Enforces guardrails: strict-JSON output contract, verdict/confidence normalization.
- Returns final output to the reviewer dashboard; LangGraph scaffolding provides the path to richer multi-agent workflows.

**Ingestion Agent (`ingestion_service` + `pdf_parser` + `chunker` + `embedding_service` + `vector_store`)**
Handles all document processing and indexing.
- Ingests medical records via a pypdf visitor capturing text, font size, font name, coordinates, and bold heuristics.
- Detects headings and tables; builds section-scoped paragraphs and sentences.
- Packs content into ~700-token chunks with 75-token overlap, enriched with diagnosis tags, medications, lab values, section priority, and a clinical-importance score.
- Generates embeddings via `text-embedding-3-large` in batches.
- Upserts chunks into a per-document Pinecone namespace with retry/backoff.

**Retrieval & Rerank (`retriever` + Pinecone hosted reranker)**
Surfaces the evidence for each criterion.
- Performs dense similarity search scoped to the claim's namespace (`top_k = 50`).
- Applies hosted `bge-reranker-v2-m3` reranking (`top_n = 12`) for precision.
- Returns ranked passages with page-level metadata for citation.

**LLM Evaluation Agent (`llm_service`)**
Performs clinical reasoning over retrieved evidence.
- Feeds reranked context plus the InterQual criterion into a strict-JSON reviewer prompt on GPT-5.5.
- Falls back automatically to gpt-5.4-mini on primary-model failure.
- Normalizes verdicts to `valid` / `doubtful` / `insufficient_evidence` and confidence to [0, 1].
- Produces structured justifications, supporting evidence with page citations, and recommended follow-up actions.

**RAGAS Scoring + Summary (`ragas_service` + `review_store`)**
Produces the nurse-ready review output.
- Computes deterministic faithfulness, answer-relevancy, context precision/recall, and utilization proxies per answer.
- Records trace ID, token usage, and latency into the MetricsRegistry.
- Aggregates per-criterion results into claim summaries (overall verdict, high-risk findings, recommended actions) and dashboard views.

## 8. Data Sources & Schema

| Data Source | Format | Content | Usage |
|---|---|---|---|
| Medical Records (`data/medical_records/`) | PDF (raw, v1–v3 samples) | Patient history, clinical notes, lab results, discharge summaries | Primary RAG input; one Pinecone namespace per record |
| InterQual Nurse Prompts (`data/jobaids/nurse_prompts_interqual.xlsx`) | Excel workbook | Nurse-authored review criteria (prompt ID, criterion text) | Query formulation for retrieval and evaluation; served at `GET /api/prompts` |
| Ground Truth (`data/gt/ground_truth_all_cases.xlsx`) | Excel workbook | Labeled expected outcomes per case | Planned production-RAGAS evaluation set |
| Pinecone Index | Vector (3072-dim, cosine) | Chunk embeddings + metadata (page, section, diagnosis/medication/lab tags, importance score) | Semantic retrieval and citation lookup |
| Review Store | In-memory | Evaluation results, claim summaries, history | Dashboard and summary APIs; audit trail within a session |
| Metrics Registry | In-memory | Request/evaluation telemetry, RAGAS scores, verdict distribution | Observability endpoints |

**Key Pydantic v2 models:** `ParsedLine` / `ParsedPage` / `ParsedDocument` (parsing), `Paragraph` / `DocumentChunk` (chunking), `NursePrompt` (criteria), `EvaluationRequest` / `EvaluationResult` / `RetrievedChunk` (evaluation), `ClaimSummary` (aggregation).

## 9. Guardrails & Safety

- **No automated decisions:** The system will not auto-deny, auto-adjust, or auto-recoup payments under any circumstance.
- **Human-in-the-loop mandatory:** Every AI output routes to nurse review for the final decision.
- **Evidence isolation:** Namespace-per-document guarantees one claim's evidence can never surface in another claim's evaluation.
- **Hallucination prevention:** The reviewer prompt is grounded strictly in reranked evidence; verdicts require page-level citations; `insufficient_evidence` is an explicit, first-class verdict rather than an inferred conclusion.
- **Output contract enforcement:** Strict-JSON responses with server-side verdict and confidence normalization; malformed outputs are rejected rather than passed downstream.
- **Resilience guardrails:** Automatic LLM fallback model; retry/backoff on vector upserts; failed requests recorded in metrics.
- **PHI / data security:** Prototype uses synthetic/sample records only. Real deployment requires access controls, encryption, audit logging, and regulatory (e.g., HIPAA) compliance.
- **No clinical advice:** The system is scoped strictly to claim review support — it does not provide diagnosis, treatment recommendations, or clinical guidance.
- **Explicit disclaimer:** Positioned as a capstone/research decision-support prototype, not a certified clinical or claims-adjudication tool.

## 10. Observability & Monitoring

Observability is built into the core: a FastAPI middleware assigns every request a request ID and captures latency; every evaluation carries a trace ID, token accounting, and RAGAS scores. LangSmith tracing is available via configuration for prompt-level debugging.

| Observability Concern | Tool / Approach |
|---|---|
| Request tracing | FastAPI middleware — request ID + latency per HTTP request |
| Evaluation tracing | Trace ID, token usage (prompt/completion), per-step latency per evaluation |
| Retrieval quality monitoring | RAGAS-style proxies — context precision/recall, utilization |
| Answer faithfulness | RAGAS-style faithfulness proxy per answer |
| Latency tracking | MetricsRegistry — p50/p95 per endpoint and end-to-end |
| Error and retry tracking | Middleware error capture + retry/backoff logging (Loguru) |
| Verdict distribution | MetricsRegistry — counts per verdict class |
| LLM prompt tracing (optional) | LangSmith — full prompt/response logging when enabled |
| Exposure | `GET /api/metrics` (snapshot) and `GET /api/observability` (combined system + RAGAS + claim view) |

## 11. Evaluation Metrics

Evaluation uses RAGAS-style metrics computed deterministically for every answer today, with the production RAGAS package planned against the ground-truth set (`data/gt`). The following metrics are tracked:

| Metric | Definition | Target |
|---|---|---|
| Context Recall | Fraction of relevant evidence passages successfully retrieved from the record | ≥ 0.85 |
| Context Precision | Fraction of retrieved passages that are actually relevant to the criterion | ≥ 0.80 |
| Answer Faithfulness | Degree to which the verdict/justification is grounded in retrieved evidence (no hallucination) | ≥ 0.90 |
| Answer Relevancy | How well the generated output answers the review criterion | ≥ 0.85 |
| Context Utilization | Fraction of provided context actually used in the answer | Monitor |
| Evidence Citation Accuracy | Percentage of citations that correctly reference the source page and passage | ≥ 0.90 |
| Verdict Accuracy (vs. ground truth) | Agreement of AI verdicts with labeled outcomes in `data/gt` | ≥ 0.80 (planned) |
| False Positive Rate | Percentage of flagged discrepancies that are incorrect (nurse-verified) | ≤ 0.15 |
| End-to-End Latency | Time from evaluation request to verdict (tracked at p50/p95) | ≤ 30 seconds |
| Token Cost per Evaluation | Prompt + completion tokens per criterion evaluation | Monitor; target downward trend |

## 12. Success Metrics

These are the business and operational outcomes that define whether the system has achieved its goals:

| Success Metric | Target | Measurement Method |
|---|---|---|
| Reduction in average claim review time | ~70% reduction vs. baseline | Compare pre/post nurse review time logs |
| Evidence retrieval accuracy | High accuracy for criterion-related queries | RAGAS context recall and precision |
| Verdict generation response time | Within seconds per criterion | MetricsRegistry latency p50/p95 |
| Reviewer satisfaction | Improvement in usefulness and trust scores | Post-session reviewer feedback surveys |
| Claim review throughput | Significant increase in claims reviewed per nurse per day | Operational productivity tracking |
| System stability under load | Stable processing of multiple records in sequence | TC-08: sequential multi-record test |
| Audit compliance | 100% of AI outputs logged with trace IDs and evidence citations | Metrics/observability endpoint completeness checks |
