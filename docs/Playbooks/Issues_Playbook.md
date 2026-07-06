# Engineering Case Log

Three issues from building the Medical AI Reviewer, written the way the reviewer itself writes a
claim up: presenting symptom → diagnosis → treatment → outcome.

---

## 01 · Table chunking broke under fitz + recursive splitting

**Type:** Retrieval quality

**Symptom**
Extracting text with `fitz` (PyMuPDF) and feeding it through a generic
`RecursiveCharacterTextSplitter` shredded tabular clinical data — rows split mid-value, lab tables
lost column alignment, and section headings got interleaved with unrelated body text.

**Diagnosis**
Character/token-count splitters don't know what a table or heading *is*. Without structural
awareness (font size, bold, coordinates) a splitter chops purely by length and destroys the
row/column relationships a reviewer needs to trust a lab value or medication line.

**Treatment**
Replaced both pieces with a purpose-built pipeline: a `PDFParser` that walks each page capturing
font size, font name, coordinates, and a bold heuristic, feeding a custom `Chunker`
(`app/services/chunking.py`) that detects headings/tables, builds section-scoped paragraphs, then
packs ~700-token chunks with 75-token overlap — tagging each chunk with diagnosis, medications,
lab values, and a clinical-importance score.

**Outcome**
Tables and section structure survive ingestion; retrieval returns chunks that read as coherent
clinical excerpts rather than fragments — which is what the two-stage retriever and reranker
depend on.

Resolved in: `Backend/app/services/chunking.py`, `Backend/app/services/pdf_parser.py`

---

## 02 · Three rounds of model selection before settling on GPT-5.5

**Type:** Iteration

**Symptom**
Round 1 (GPT-4o): the reviewer returned high confidence on almost every criterion, valid or not —
overconfident verdicts a nurse reviewer couldn't trust at face value. Round 2 (GPT-5 Mini):
confidence came down, but reasoning was shallow — justifications didn't hold up against ambiguous
or contradictory evidence.

**Diagnosis**
Confidence calibration and reasoning depth trade off against model size. Neither extreme fit an
evidence-grounded, auditable review: one over-trusted itself, the other under-reasoned.

**Treatment**
Checked which chat models the project's OpenAI key actually had access to, and selected the most
capable, stable version available — `gpt-5.5` — as the primary reviewer, with `gpt-5.4-mini` wired
in as an automatic fallback in `LLMService._invoke_with_fallback` if the primary call errors.

```
# Backend/.env
OPENAI_MODEL=gpt-5.5
OPENAI_FALLBACK_MODEL=gpt-5.4-mini
```

**Outcome**
Verdicts now normalize confidence and fall back to `doubtful` / `insufficient_evidence` when the
model itself signals uncertainty, instead of defaulting to blanket high confidence.

Resolved in: `Backend/.env`, `Backend/app/services/llm_service.py`

---

## 03 · Backend.app imports broke the Docker build

**Type:** Blocking

**Symptom**
Every backend module imports with the full package prefix — `from Backend.app.core.config import
settings`, `from Backend.app.services.vector_store import VectorStore`, and so on. Building the
image with a Docker context rooted at `Backend/` (the natural instinct) copied the app in without
that outer `Backend` folder, so every one of those imports failed at container start.

**Diagnosis**
The import paths and the Docker build context disagreed about where the package root was. Fixing
the imports would mean touching dozens of files; fixing the build context meant changing three
lines.

**Treatment**
Set the Docker build context to the repository root (not `Backend/`) in `docker-compose.yml`, and
in `Backend/Dockerfile` copy the folder in a way that keeps the `Backend/` prefix intact on disk
inside the image, so `Backend.app.xxx` resolves exactly like it does locally.

```
# docker-compose.yml
build:
  context: .                # repo root, not ./Backend
  dockerfile: Backend/Dockerfile
```

```
# Backend/Dockerfile
WORKDIR /app
# Keep the Backend/ prefix intact so "Backend.app.xxx" imports keep working
COPY Backend ./Backend
COPY data ./data
CMD ["sh", "-c", "uvicorn Backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

**Outcome**
No import changes needed anywhere in the codebase — the container's file layout now just matches
what the imports already expected.

Resolved in: `docker-compose.yml`, `Backend/Dockerfile`
