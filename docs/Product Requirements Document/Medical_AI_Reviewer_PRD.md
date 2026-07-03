# Medical AI Reviewer – Product Requirements Document (PRD)

## Overview

Insurance companies review already-paid claims to make sure providers billed correctly and that the medical record supports the payment. Today, this work is done manually by nurses, who must read long patient records, find the relevant clinical details, and check whether the billed services are justified.

This process is slow and hard to scale because medical records can be over 1,000 pages long. A nurse may review only 4–5 claims per day, while insurers may receive thousands of claims for review daily. This leads to high review costs, slower turnaround, and missed opportunities to detect overpayments or unsupported claims.

Medical AI Reviewer is an AI-powered claim review assistant built on an **agentic, evidence-grounded Retrieval-Augmented Generation (RAG) system**. It ingests raw medical-record PDFs, indexes them into a vector database, and evaluates them against a curated library of **nurse-authored InterQual review criteria**. For every criterion it returns a verdict (`valid` / `doubtful` / `insufficient_evidence`), a confidence score, an evidence-grounded justification with page citations, and recommended follow-up actions — all surfaced through an Angular reviewer dashboard.

The goal is to reduce manual reading time and help nurses focus on decision-making instead of searching through documents. The nurse remains the final reviewer, while the AI acts as a first-pass assistant that speeds up the process and improves efficiency. **Traceability, auditability, and observability are first-class citizens**: every evaluation carries a trace ID, token accounting, latency telemetry, and RAGAS-style retrieval-quality metrics.

**One-line summary:** Medical AI Reviewer helps insurance nurses review claims faster by reading large medical records, evaluating them against InterQual criteria, and returning evidence-cited verdicts — while the nurse makes the final call.

## Problem Statement

- Large medical records can exceed 1,000 pages, making reviews slow and difficult.
- A nurse can review only about 4–5 claims per day, while thousands of claims may require review daily.
- The process depends on trained clinical reviewers, making it expensive to scale.
- Slow reviews can delay recovery actions and increase the chance of missed discrepancies.
- Manual review of large records can lead to inconsistent outcomes across reviewers.

## Proposed Solution

Medical AI Reviewer is a Retrieval-Augmented Generation (RAG) system designed to support post-payment claim review. It reads patient medical records, retrieves the evidence relevant to each InterQual review criterion, evaluates the criterion with a grounded LLM verdict, and presents an evidence-cited summary to the nurse reviewer.

The goal is to shift the nurse's role from reading everything manually to reviewing AI-prepared evidence and making the final decision.

### What the system does

- Ingests medical-record PDFs with **structure-aware parsing** (font, coordinate, and bold heuristics to reconstruct headings, sections, and tables).
- Splits records into **clinical-aware chunks** (~700 tokens, 75-token overlap) tagged with diagnoses, medications, lab values, and a clinical-importance score.
- Embeds and indexes chunks in **Pinecone**, with one namespace per document so evidence never leaks across claims.
- Retrieves evidence per criterion using **two-stage retrieval**: dense search (top-50) followed by hosted BGE reranking (top-12).
- Evaluates each criterion with a **grounded GPT-5.5 reviewer** (strict JSON, automatic fallback model) returning verdict, confidence, page-cited justification, and recommended actions.
- Aggregates per-criterion results into a **claim summary** with high-risk findings, and exposes all reviewed claims on a dashboard.
- Scores every answer with **RAGAS-style metrics** (faithfulness, answer relevancy, context precision/recall) and records full request/evaluation telemetry.

## Goals

### Business Goals

- Reduce claim review turnaround time.
- Increase reviewer productivity.
- Lower manual review effort and operational cost.
- Improve coverage of high claim review volumes.

### Functional Goals

- Ingest and process large medical records.
- Retrieve relevant evidence for each InterQual review criterion.
- Return a normalized verdict with confidence and page-cited justification per criterion.
- Generate concise, evidence-backed claim summaries for nurse reviewers.
- Provide full observability: latency (p50/p95), error rates, token usage, verdict distribution, and retrieval-quality metrics.

## Non-Goals

- No automated claim decisions — the system will not auto-deny, auto-adjust, or auto-recoup payments.
- No replacement of nurse reviewers — final judgment remains with the human reviewer.
- No diagnosis or medical advice — the system is only for claim review support, not clinical decision-making.
- Not a system of record — it reads records and claim data but does not replace EHR or claims systems.
- No provider-side coding or billing actions.

## Feature Definition

| Feature | Description | Priority | Status |
|---|---|---|---|
| Document Upload | Upload medical-record PDFs via drag-and-drop; parsed, chunked, embedded, and indexed automatically (`POST /api/upload`). | High | ✅ Implemented |
| Document Parsing & Chunking | Structure-aware pypdf parsing (font/coordinate/bold heuristics) and clinical-aware chunking (~700 tokens, 75 overlap, diagnosis/medication/lab tags, clinical-importance score). | High | ✅ Implemented |
| Embedding Generation | OpenAI `text-embedding-3-large` (3072-dim), batched. | High | ✅ Implemented |
| Vector Database | Pinecone serverless index (cosine) with one **namespace per document** for claim isolation; retry/backoff upserts. | High | ✅ Implemented |
| RAG Retrieval | Two-stage retrieval: dense top-k = 50 followed by hosted `bge-reranker-v2-m3` to top-n = 12. | High | ✅ Implemented |
| InterQual Criteria Library | Nurse-authored review criteria loaded from the Excel job aid and served via `GET /api/prompts`. | High | ✅ Implemented |
| Evidence-Grounded Evaluation | GPT-5.5 strict-JSON reviewer (fallback gpt-5.4-mini): verdict (`valid`/`doubtful`/`insufficient_evidence`), confidence, justification, evidence with page citations, follow-up actions. | High | ✅ Implemented |
| Evidence Highlighting & Citations | Evidence cards with page-level references shown next to an in-browser PDF viewer for explainability and auditability. | High | ✅ Implemented |
| AI Claim Summary | Aggregated claim summary: overall verdict, confidence, high-risk findings, recommended actions (`GET /api/claims/{namespace}/summary`). | High | ✅ Implemented |
| Reviewer Dashboard | Angular 22 dashboard: all reviewed claims, stat cards, side-by-side review, upload flow. | Medium | ✅ Implemented |
| Observability & Metrics | Request tracing middleware, trace IDs, token accounting, latency p50/p95, error rates, verdict distribution, RAGAS metrics (`/api/metrics`, `/api/observability`). | High | ✅ Implemented |
| RAGAS Evaluation | Deterministic faithfulness, answer-relevancy, context precision/recall, and utilization proxies per answer; production RAGAS against the ground-truth set planned. | High | ✅ Implemented (proxies) |


## Project Type

**Primary Type:** Medical Document Summarizer + Clinical Evidence Recommender

- Summarization of lengthy medical records into concise reviewer-friendly outputs with per-criterion verdicts.
- Recommendation of relevant evidence and flagged discrepancies to help nurse reviewers validate claims faster.

This places the system in the category of **AI-augmented decision support** — not autonomous decision-making. The AI prepares, organises, and highlights; the nurse decides.

## Tech Stack

The following table explains the rationale behind the technology stack **implemented** in the Medical AI Reviewer project. Technologies were chosen based on retrieval quality at scale, production-style engineering practice, observability, and suitability for an evidence-grounded RAG application.

| **Layer** | **Selected Technology** | **Justification** | **Why Not Other Options?** |
| --- | --- | --- | --- |
| **User Interface** | **Angular 22 + Angular Material** | A production-grade SPA with standalone components, typed API services, routing, and rich components (PDF viewer, drag-and-drop upload, stat/evidence cards). Enables a real reviewer workflow: dashboard grid, side-by-side PDF review, and claim summaries. | **Streamlit** (originally planned) is excellent for prototypes but limited in customisation, routing, and component reuse for a multi-view reviewer product. **React/Vue** are viable but Angular's batteries-included structure (DI, router, Material) suited a structured dashboard best. |
| **Backend** | **Python + FastAPI (Uvicorn)** | Modern async framework with automatic OpenAPI docs, Pydantic v2 validation, dependency injection, and middleware hooks used for request-level observability. Native fit with the AI ecosystem. | **Flask** lacks native async and validation. **Django** carries unnecessary weight for an AI-pipeline API. **Node.js** has a smaller AI ecosystem. |
| **Document Processing** | **pypdf (structure-aware) + tiktoken** | A custom pypdf visitor captures text with font size, font name, coordinates, and bold heuristics, letting the chunker reconstruct headings, sections, and tables; tiktoken enforces token budgets for chunking and cost control. | Plain-text extraction loses the clinical document structure that drives chunk quality. **Unstructured/Tika** are heavier; **OCR (Tesseract)** deferred as a future enhancement since prototype records are digital PDFs. |
| **Embeddings** | **OpenAI `text-embedding-3-large`** | High retrieval quality at 3072 dimensions, no local GPU/inference infrastructure required, consistent with the OpenAI chat stack, and simple batched API usage. | **HuggingFace BGE** (originally planned) requires local inference resources and a re-embedding pipeline on model updates. BGE is still used where it shines — as the hosted **reranker**. |
| **Vector Database** | **Pinecone (serverless)** | Managed, persistent vector store with metadata, **namespaces** (one per document — the claim-isolation mechanism), and **hosted `bge-reranker-v2-m3`** reranking, removing the need to host a cross-encoder. | **FAISS/ChromaDB** (originally planned) are in-memory/local, lack managed persistence and hosted reranking, and complicate namespace-style isolation. **Milvus/Weaviate** need extra infrastructure. |
| **Large Language Model** | **GPT-5.5 (fallback: gpt-5.4-mini)** | Strong reasoning over clinical text, reliable strict-JSON output for verdict/confidence/citations, and an automatic cheaper fallback model for resilience and cost control. | **Open-source LLMs** require GPU infrastructure. Smaller models produce weaker grounded reasoning on 12-chunk clinical contexts. |
| **Storage** | **In-memory ReviewStore (prototype)** | Fast iteration for a capstone: claims, summaries, and history held in process, exposed via dashboard/summary APIs. Designed as a single seam to swap for a database. | **PostgreSQL** (originally planned) remains the production path; deferred to keep the prototype focused on the RAG pipeline. **SQLite** wouldn't demonstrate the swap-out seam any better. |
| **Monitoring** | **MetricsRegistry + Loguru (+ optional LangSmith)** | Built-in request middleware assigns request IDs and captures latency; evaluations carry trace IDs, token accounting, verdict distribution, and RAGAS scores — all queryable at `/api/metrics` and `/api/observability`. LangSmith tracing is available via config. | **Prometheus/Grafana** monitor infrastructure, not LLM workflow quality. Relying on LangSmith alone would externalise data and add cost; the in-app registry keeps core telemetry local. |
| **Evaluation** | **RAGAS-style deterministic proxies** | Faithfulness, answer relevancy, context precision/recall, and utilization computed per answer with zero extra LLM cost, giving continuous retrieval-quality signal. Production RAGAS against `data/gt/ground_truth_all_cases.xlsx` is planned. | **BLEU/ROUGE** measure text similarity, not grounding or retrieval quality. Full RAGAS on every request adds LLM cost/latency; proxies give an always-on signal first. |
| **Deployment** | **Docker + docker-compose** | Containerised backend and UI with consistent execution across environments; simple local orchestration. | Direct cloud deployment (**AWS/Azure/GCP**) adds infrastructure setup beyond capstone scope; compose keeps the system reproducible anywhere. |

---

## Test Cases

| Test ID | Scenario | Expected Result |
|---|---|---|
| TC-01 | Upload a valid PDF medical record via `POST /api/upload` | File is parsed, chunked, embedded, and upserted; response contains `document_id`, `namespace`, and chunk count |
| TC-02 | Upload a very large (1000+ page) medical record | File is ingested and indexed successfully within token budgets |
| TC-03 | List review criteria via `GET /api/prompts` | All InterQual nurse prompts from the job aid are returned |
| TC-04 | Evaluate a criterion via `POST /api/evaluate` | Relevant evidence is retrieved and reranked; a normalized verdict with confidence, justification, and page citations is returned |
| TC-05 | Evaluate a criterion with inconsistent or missing documentation | Verdict of `doubtful` or `insufficient_evidence` is returned with justification rather than a fabricated `valid` |
| TC-06 | Upload an invalid or unsupported file | System returns an appropriate error message |
| TC-07 | Request a claim summary via `GET /api/claims/{namespace}/summary` | Aggregated verdict, confidence, high-risk findings, and recommended actions are returned |
| TC-08 | Upload and evaluate multiple records in sequence | System remains stable; each claim's evidence stays isolated in its own namespace |
| TC-09 | Primary LLM call fails | System automatically falls back to the fallback model and completes the evaluation |
| TC-10 | Query `GET /api/metrics` and `GET /api/observability` after evaluations | Latency p50/p95, error rates, token usage, verdict distribution, and RAGAS metrics are reported |

## Success Metrics

- Reduce average review time per claim by ~70%.
- Achieve high evidence retrieval accuracy for claim-related queries (RAGAS context precision/recall).
- Generate verdicts and summaries within seconds per criterion (tracked at p50/p95).
- Maintain high groundedness: RAGAS faithfulness on every answer, with page-cited evidence on 100% of verdicts.
- Improve reviewer satisfaction with usefulness and trust of AI outputs.
