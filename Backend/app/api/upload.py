import os
import os
import uuid

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from Backend.app.core.dependencies import get_ingestion_service
from Backend.app.core.logging import logger
from Backend.app.db.review_store import review_store
from Backend.app.models.api_models import UploadResponse
from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/api",
    tags=["Upload"],
)

UPLOAD_FOLDER = "medical_records"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Maps the detection tags to exact sheet names in the nurse-prompt workbook.
_DIAGNOSIS_TAG_TO_SHEET: dict[str, str] = {
    "COVID":     "COVID-19",
    "CHF":       "CHF-ADHF",
    "SEPSIS":    "Sepsis",
    "PNEUMONIA": "CAP",
    "COPD":      "AECOPD",
    "NSTEMI":    "NSTEMI-ACS",
    "PE":        "Pulmonary Embolism",
    "STROKE":    "Ischemic Stroke",
}

# Weighted keyword rules — scored across the FULL document text.
# Rules are (keyword, tag, weight).
# Longer/more specific phrases get higher weight so they dominate over
# incidental single-word mentions.
_DIAGNOSIS_RULES: list[tuple[str, str, int]] = [
    # ── Highest weight: explicit multi-word diagnosis phrases ──────────────
    ("community-acquired pneumonia",            "PNEUMONIA", 100),
    ("community acquired pneumonia",            "PNEUMONIA", 100),
    ("acute exacerbation of copd",              "COPD",      100),
    ("acute exacerbation copd",                 "COPD",      100),
    ("aecopd",                                  "COPD",      100),
    ("copd exacerbation",                       "COPD",      100),
    ("congestive heart failure",                "CHF",       100),
    ("acute decompensated heart failure",       "CHF",       100),
    ("non-st elevation myocardial infarction",  "NSTEMI",    100),
    ("non st elevation myocardial infarction",  "NSTEMI",    100),
    ("acute coronary syndrome",                 "NSTEMI",    100),
    ("pulmonary embolism",                      "PE",        100),
    ("pulmonary embolus",                       "PE",        100),
    ("deep vein thrombosis",                    "PE",        100),
    ("venous thromboembolism",                  "PE",        100),
    ("ischemic stroke",                         "STROKE",    100),
    ("cerebrovascular accident",                "STROKE",    100),
    ("transient ischemic attack",               "STROKE",    100),
    ("septic shock",                            "SEPSIS",    100),
    ("severe sepsis",                           "SEPSIS",    100),
    ("covid-19",                                "COVID",     100),
    ("sars-cov-2",                              "COVID",     100),
    ("novel coronavirus",                       "COVID",     100),

    # ── High weight: specific but shorter phrases ─────────────────────────
    ("myocardial infarction",   "NSTEMI",    60),
    ("heart failure",           "CHF",       60),
    ("chronic obstructive pulmonary", "COPD", 60),
    ("chronic obstructive",     "COPD",      60),
    ("chronic bronchitis",      "COPD",      60),
    ("hypercapnic respiratory", "COPD",      60),
    ("obstructive lung disease","COPD",      60),
    ("systolic heart failure",  "CHF",       60),
    ("diastolic heart failure", "CHF",       60),
    ("decompensated heart",     "CHF",       60),
    ("reduced ejection fraction","CHF",      60),
    ("cardiomyopathy",          "CHF",       60),
    ("cerebral infarction",     "STROKE",    60),
    ("brain infarction",        "STROKE",    60),
    ("unstable angina",         "NSTEMI",    60),
    ("troponin elevation",      "NSTEMI",    60),
    ("elevated troponin",       "NSTEMI",    60),
    ("systemic inflammatory response", "SEPSIS", 60),
    ("bacteremia",              "SEPSIS",    60),
    ("pneumonitis",             "PNEUMONIA", 60),

    # ── Medium weight: primary diagnosis keywords ─────────────────────────
    ("pneumonia",       "PNEUMONIA", 40),
    ("copd",            "COPD",      40),
    ("emphysema",       "COPD",      40),
    ("sepsis",          "SEPSIS",    40),
    ("nstemi",          "NSTEMI",    40),
    ("cardiac failure", "CHF",       40),
    ("chf",             "CHF",       40),
    ("adhf",            "CHF",       40),
    ("hfref",           "CHF",       40),
    ("hfpef",           "CHF",       40),
    ("stroke",          "STROKE",    40),
    ("cerebrovascular", "STROKE",    40),
    ("covid",           "COVID",     40),
    ("coronavirus",     "COVID",     40),
    ("dvt",             "PE",        40),
    ("vte",             "PE",        40),
    ("thromboembolism", "PE",        40),

    # ── Lower weight: short/ambiguous terms ───────────────────────────────
    ("heart attack",    "NSTEMI",    20),
    ("acute coronary",  "NSTEMI",    20),
    ("ischemic heart",  "NSTEMI",    20),
    ("angina",          "NSTEMI",    20),
    ("cva",             "STROKE",    20),
    ("tia",             "STROKE",    20),
    ("septicemia",      "SEPSIS",    20),
    ("lung infection",  "PNEUMONIA", 20),
    ("brain attack",    "STROKE",    20),
    ("blood clot",      "PE",        20),
    ("covid19",         "COVID",     20),
]


def _detect_top_diagnosis(chunks: list[DocumentChunk]) -> str | None:
    """
    Score the full document text against weighted keyword rules and return the
    sheet name of the highest-scoring diagnosis.  Returns None when no
    keyword matches anywhere in the document.

    This approach is more accurate than per-chunk first-match tallying because:
    - Longer, more specific phrases score much higher than short ones
    - Each keyword is counted once per occurrence across the whole document
    - A single "congestive heart failure" outweighs 10 incidental "angina" mentions
    """
    if not chunks:
        return None

    # Concatenate all chunk text for whole-document analysis
    full_text = " ".join(
        c.text.lower() for c in chunks if c.text
    )

    if not full_text.strip():
        return None

    # Accumulate weighted scores per tag
    scores: dict[str, int] = {}
    for keyword, tag, weight in _DIAGNOSIS_RULES:
        count = full_text.count(keyword)
        if count:
            scores[tag] = scores.get(tag, 0) + count * weight

    if not scores:
        return None

    top_tag = max(scores, key=lambda t: scores[t])
    return _DIAGNOSIS_TAG_TO_SHEET.get(top_tag, top_tag)


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_pdf(
    file: UploadFile = File(...),
    service: IngestionService = Depends(get_ingestion_service),
) -> UploadResponse:
    document_id = str(uuid.uuid4())
    namespace = document_id
    filename = f"{document_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Write file asynchronously so the event loop is not blocked
    try:
        content = await file.read()
        async with aiofiles.open(filepath, "wb") as buffer:
            await buffer.write(content)
    except Exception as exc:
        logger.bind(filename=file.filename, error=str(exc)).error("file_write_failed")
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {exc}")

    # Ingest into Pinecone; clean up the saved file on failure
    try:
        chunks = await service.ingest(filepath, namespace=namespace)
    except Exception as exc:
        logger.bind(
            document_id=document_id,
            filename=file.filename,
            error=str(exc),
        ).error("ingestion_failed")
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {exc}")

    review_store.register_claim(
        document_id=document_id,
        namespace=namespace,
        filename=file.filename,
        pdf_path=filepath,
    )

    # Detect the top diagnosis from chunk tags so the UI can pre-filter prompts
    detected_diagnosis = _detect_top_diagnosis(chunks)

    logger.bind(
        document_id=document_id,
        namespace=namespace,
        filename=file.filename,
        chunks=len(chunks),
        detected_diagnosis=detected_diagnosis,
    ).info("medical_record_uploaded")

    return UploadResponse(
        document_id=document_id,
        namespace=namespace,
        filename=file.filename,
        pdf_path=filepath,
        chunks=len(chunks),
        message="Document uploaded successfully",
        detected_diagnosis=detected_diagnosis,
    )