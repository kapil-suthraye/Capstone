# Medical AI Reviewer – Product Requirements Document (PRD)

## Overview

Insurance companies review already-paid claims to make sure providers billed correctly and that the medical record supports the payment. Today, this work is done manually by nurses, who must read long patient records, find the relevant clinical details, and check whether the billed services are justified.

This process is slow and hard to scale because medical records can be over 1,000 pages long. A nurse may review only 4–5 claims per day, while insurers may receive thousands of claims for review daily. This leads to high review costs, slower turnaround, and missed opportunities to detect overpayments or unsupported claims.

Medical AI Reviewer is an AI-powered claim review assistant built on a Retrieval-Augmented Generation (RAG) system. It reads the medical record, finds the most relevant evidence for each claim line item, highlights possible discrepancies, and generates a short evidence-backed summary for the reviewer.

The goal is to reduce manual reading time and help nurses focus on decision-making instead of searching through documents. The nurse remains the final reviewer, while the AI acts as a first-pass assistant that speeds up the process and improves efficiency.

**One-line summary:** Medical AI Reviewer helps insurance nurses review claims faster by reading large medical records, finding supporting evidence, and flagging possible discrepancies.

## Problem Statement

- Large medical records can exceed 1,000 pages, making reviews slow and difficult.
- A nurse can review only about 4–5 claims per day, while thousands of claims may require review daily.
- The process depends on trained clinical reviewers, making it expensive to scale.
- Slow reviews can delay recovery actions and increase the chance of missed discrepancies.
- Manual review of large records can lead to inconsistent outcomes across reviewers.

## Proposed Solution

Medical AI Reviewer is a Retrieval-Augmented Generation (RAG) system designed to support post-payment claim review. It reads patient medical records, finds the evidence relevant to each claim, identifies possible discrepancies, and presents a concise summary to the nurse reviewer.

The goal is to shift the nurse’s role from reading everything manually to reviewing AI-prepared evidence and making the final decision.

### What the system does

- Process large medical records efficiently.
- Extract and highlight relevant evidence for each billed claim item.
- Identify possible discrepancies in services, codes, dates, units, and documentation.
- Generate a concise reviewer-friendly summary with evidence citations.

## Goals

### Business Goals

- Reduce claim review turnaround time.
- Increase reviewer productivity.
- Lower manual review effort and operational cost.
- Improve coverage of high claim review volumes.

### Functional Goals

- Ingest and process large medical records.
- Retrieve relevant evidence for each billed claim item.
- Flag possible discrepancies in claims and documentation.
- Generate concise, evidence-backed summaries for nurse reviewers.

## Non-Goals

- No automated claim decisions — the system will not auto-deny, auto-adjust, or auto-recoup payments.
- No replacement of nurse reviewers — final judgment remains with the human reviewer.
- No diagnosis or medical advice — the system is only for claim review support, not clinical decision-making.
- Not a system of record — it reads records and claim data but does not replace EHR or claims systems.
- No provider-side coding or billing actions.

## Feature Definition

| Feature | Description | Priority |
|---|---|---|
| Document Upload | Upload medical records and related claim documents in supported formats such as PDF and DOC. | High |
| OCR Support | Extract text from scanned or image-based medical records. | High |
| Document Parsing & Chunking | Break large records into structured sections and smaller chunks for processing. | High |
| Embedding Generation | Convert document chunks into vector embeddings for semantic retrieval. | High |
| Vector Database | Store embeddings and metadata for fast evidence retrieval. | High |
| RAG Retrieval | Retrieve the most relevant passages from the medical record for each claim review task. | High |
| Evidence Extraction | Extract supporting or contradicting evidence related to billed services, codes, dates, and medical necessity. | High |
| Discrepancy Detection | Identify possible mismatches, missing documentation, unsupported claims, or coding inconsistencies. | High |
| AI Summary Generation | Generate a concise, evidence-backed summary for the nurse reviewer. | High |
| Evidence Highlighting & Citations | Show relevant source passages with page-level references for explainability and auditability. | High |
| Reviewer Dashboard | Display review status, findings, flagged discrepancies, and supporting evidence in one place. | Medium |
| Reviewer Q&A / Chat | Allow reviewers to ask follow-up questions about the claim or medical record. | Medium |
| Feedback Loop | Capture reviewer corrections and feedback to improve prompts, rules, or future system performance. | Medium |
| Audit Logs | Record system actions, retrieved evidence, AI outputs, and reviewer decisions for traceability. | High |

## Project Type

**Primary Type:** Medical Document Summarizer + Clinical Evidence Recommender

- Summarization of lengthy medical records into concise reviewer-friendly outputs.
- Recommendation of relevant evidence and discrepancies to help nurse reviewers validate claims faster.

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Reviewer interface / prototype UI |
| Backend | Python | Core application and AI pipeline logic |
| Document Parsing | PyPDF / Unstructured | Extract and process text from medical records |
| Embeddings | HuggingFace BGE | Convert document chunks into vector embeddings |
| Vector Store | FAISS | Store and retrieve semantic search results |
| AI Model | GPT-4o / Claude / Llama | Evidence analysis, summarization, and discrepancy detection |
| RAG Framework | LangChain | Orchestrate retrieval and LLM workflow |
| Storage | Local Files / PostgreSQL | Store uploaded files, metadata, and review data |
| Observability | LangSmith | Trace prompts, retrieval, and model outputs |
| Evaluation | RAGAS | Evaluate retrieval and answer quality |

## Test Cases

| Test ID | Scenario | Expected Result |
|---|---|---|
| TC-01 | Upload a valid PDF medical record | File is uploaded and processed successfully |
| TC-02 | Upload a 1000+ page medical record | File is ingested and indexed successfully |
| TC-03 | Ask a question about a medical record | Relevant evidence is retrieved and returned |
| TC-04 | Generate a claim review summary | Summary is produced with supporting evidence |
| TC-05 | Review a claim with inconsistent documentation | Possible discrepancy is detected and highlighted |
| TC-06 | Upload an invalid or unsupported file | System shows an appropriate error message |
| TC-07 | Process a record with missing patient or claim data | System shows a warning or incomplete-data flag |
| TC-08 | Upload multiple records or claims in sequence | System remains stable and processes them successfully |
| TC-09 | Attempt access with unauthorized credentials | Access is denied |
| TC-10 | Submit reviewer feedback or correction | Feedback is saved successfully |

## Success Metrics

- Reduce average review time per claim by ~70%.
- Achieve high evidence retrieval accuracy for claim-related queries.
- Generate responses and summaries within a few seconds.
- Improve reviewer satisfaction with usefulness and trust of AI outputs.
