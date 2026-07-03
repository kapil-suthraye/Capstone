# Medical AI Reviewer - High Level Architecture Explanation

## Overview

The Medical AI Reviewer is a Generative AI-based solution designed to assist insurance companies in validating healthcare claims. Currently, claim validation requires nurses to manually review large medical records, which can contain hundreds or thousands of pages. This process is time-consuming, expensive, and difficult to scale.

The implemented solution is an **agentic, evidence-grounded RAG system** that ingests raw medical-record PDFs, indexes them into a Pinecone vector database, and evaluates them against a curated library of **nurse-authored InterQual review criteria**. For every criterion it returns a verdict (`valid` / `doubtful` / `insufficient_evidence`), a confidence score, an evidence-grounded justification with page citations, and recommended follow-up actions. The nurse remains the final decision maker, ensuring a human-in-the-loop approach.

---

# High Level Architecture

```text
Insurance Claim Review
          │
          ▼
Medical Records (raw PDFs)
          │  POST /api/upload
          ▼
Medical AI Reviewer Platform (FastAPI)
  Parse ▸ Chunk ▸ Embed ▸ Upsert (Pinecone namespace per document)
  Retrieve (top-50) ▸ Rerank (BGE, top-12) ▸ LLM Verdict ▸ RAGAS Scoring
          │
          ▼
Nurse Dashboard (Angular 22)
  Upload · Dashboard · Side-by-side Review · Claim Summary
          │
          ▼
Final Decision (Human-in-the-Loop)
```

---

# Component Details

## 1. Insurance Claim Review

### Purpose

This is the starting point of the workflow. The insurance company initiates a review request for a previously processed healthcare claim.

### Inputs

* Claim medical-record PDF (uploaded via the dashboard)
* InterQual review criteria (nurse-authored, loaded from the Excel job aid `data/jobaids/nurse_prompts_interqual.xlsx`)
* A unique `document_id` / Pinecone `namespace` assigned at upload, which scopes all evidence to that claim

### Business Challenge

A large number of claims require validation daily, creating significant workload for nursing staff. A nurse can review only 4–5 claims per day against thousands received.

---

## 2. Medical Records

### Purpose

Medical records serve as the primary evidence source used to validate claim authenticity.

### Examples

* Patient History
* Doctor Notes
* Diagnosis Reports
* Treatment Records
* Lab Reports
* Discharge Summaries
* Clinical Documentation

### Challenges

* Records may contain hundreds or thousands of pages.
* Information is often unstructured and layout-heavy (headings, sections, tables).
* Important evidence may be scattered across the document.

### How the system addresses this

* **Structure-aware parsing** captures font size, font name, coordinates, and bold heuristics to reconstruct document structure, rather than extracting flat text.
* **Clinical-aware chunking** produces ~700-token, section-scoped chunks (75-token overlap) tagged with diagnoses, medications, lab values, and a clinical-importance score.

---

## 3. Medical AI Reviewer Platform

### Purpose

The Medical AI Reviewer Platform is the core intelligence layer of the solution. It automates the review process by extracting relevant evidence from medical records and evaluating each InterQual criterion with a grounded LLM verdict.

---

### 3.1 Document Processing (Ingestion)

#### Objective

Convert large medical documents into machine-readable, retrieval-ready content.

#### Activities

* PDF ingestion via `POST /api/upload`
* Structure-aware text extraction (pypdf visitor: text + font + coordinates + bold heuristic)
* Heading/table detection and section-scoped paragraph building
* Token-budgeted clinical chunking (tiktoken)
* Embedding (OpenAI `text-embedding-3-large`, 3072-dim) and upsert into a per-document Pinecone namespace

#### Implemented Technologies

* Python (FastAPI service layer)
* pypdf, tiktoken
* OpenAI embeddings, Pinecone
* OCR — *future enhancement (scanned records are out of scope for the prototype)*

---

### 3.2 Evidence Extraction (Retrieval & Reranking)

#### Objective

Identify the passages of the record most relevant to each review criterion.

#### How it works

* Dense similarity search over the claim's Pinecone namespace (`top_k = 50`) for high recall
* Hosted **BGE reranking** (`bge-reranker-v2-m3`, `top_n = 12`) for precision
* Retrieved chunks carry page numbers, section context, and clinical tags for citation

#### Implemented Technologies

* Pinecone serverless vector database (cosine, 3072-dim, namespaces)
* Pinecone-hosted BGE reranker
* LangChain / LangGraph orchestration scaffolding

---

### 3.3 Discrepancy Detection (LLM Evaluation)

#### Objective

Compare each InterQual criterion against the retrieved medical evidence and identify whether the claim is supported.

#### Example Scenarios

* Criterion satisfied and clearly documented → `valid`
* Documentation partially supports the criterion or conflicts → `doubtful`
* No relevant evidence found in the record → `insufficient_evidence`

#### Implemented Technologies

* OpenAI **GPT-5.5** reviewer with automatic fallback to **gpt-5.4-mini**
* Strict-JSON output contract with verdict/confidence normalization
* Retrieval-Augmented Generation (RAG): the model sees only reranked evidence from the claim's own namespace

---

### 3.4 Summary Generation

#### Objective

Generate a concise nurse-friendly summary containing key findings.

#### Output Includes

* Per-criterion verdicts with confidence scores
* Evidence-grounded justifications with page citations
* High-risk findings
* Recommended follow-up actions
* Claim-level aggregate summary (`GET /api/claims/{namespace}/summary`)

#### Implemented Technologies

* GPT-5.5 (strict-JSON prompting)
* ReviewStore aggregation (claims, summaries, dashboard views)
* RAGAS-style scoring per answer (faithfulness, relevancy, context precision/recall)

---

## 4. Nurse Dashboard

### Purpose

Provide nurses with an easy-to-review, evidence-backed workspace generated by the AI platform.

### Features

* Drag-and-drop PDF upload with progress
* Dashboard grid of all reviewed claims with stat cards
* Side-by-side review: source PDF (in-browser viewer) next to AI evidence cards
* Per-claim summary: overall verdict, high-risk findings, recommended actions

### Benefits

* Reduces manual reading effort
* Improves review efficiency and consistency
* Maintains human oversight — every AI finding is verifiable against the cited page

### Implemented Technologies

* Angular 22 (standalone components, SSR-ready), Angular Material + CDK
* ngx-extended-pdf-viewer, ngx-file-drop

---

## 5. Final Decision

### Purpose

The final decision remains with the nurse or claim reviewer.

### Possible Outcomes

* Approve Claim
* Reject Claim
* Escalate for Further Investigation

### Importance

This ensures regulatory compliance and preserves human accountability within the review process. The system is explicitly a decision-support prototype — it never auto-adjudicates, and every verdict carries citations so the nurse can verify before acting.

---

# Implemented Technology Stack

| Layer               | Technology                                              |
| ------------------- | ------------------------------------------------------- |
| Frontend            | Angular 22 + Angular Material                            |
| Backend             | Python + FastAPI (Uvicorn)                               |
| Document Processing | pypdf (structure-aware), tiktoken                        |
| Embeddings          | OpenAI `text-embedding-3-large` (3072-dim)               |
| Vector Database     | Pinecone serverless (cosine, namespace per document)     |
| Reranking           | Pinecone-hosted `bge-reranker-v2-m3`                     |
| RAG Framework       | LangChain / LangGraph                                    |
| LLM                 | OpenAI GPT-5.5 (fallback: gpt-5.4-mini)                  |
| Observability       | MetricsRegistry + Loguru (+ optional LangSmith tracing)  |
| Evaluation          | RAGAS-style deterministic proxies                        |
| Criteria Source     | InterQual nurse prompts (Excel job aid, via openpyxl)    |
| Review Storage      | In-memory ReviewStore (prototype)                        |
| Deployment          | Docker + docker-compose                                  |

---

# Expected Benefits

* Faster claim review process
* Reduced manual effort for nurses
* Improved scalability
* Lower operational costs
* Faster identification of discrepancies
* Improved claim validation accuracy and consistency
* Full traceability: trace IDs, token accounting, latency telemetry, and retrieval-quality metrics on every evaluation

---

## Conclusion

The Medical AI Reviewer augments healthcare claim reviewers by automating document analysis and evidence discovery. By combining structure-aware ingestion, two-stage retrieval, grounded LLM verdicts, and built-in observability with human validation, the solution significantly improves review efficiency while maintaining trust, compliance, and accountability.
