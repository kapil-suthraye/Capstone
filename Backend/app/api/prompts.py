from fastapi import APIRouter, Depends, Query

from Backend.app.core.dependencies import get_nurse_prompt_loader
from Backend.app.models.nurse_prompt import NursePrompt
from Backend.app.services.nurse_prompts import NursePromptLoader

router = APIRouter(
    prefix="/api",
    tags=["Prompts"],
)

# ---------------------------------------------------------------------------
# Synonym map  →  exact sheet names as they appear in the workbook
# Keys are lower-cased query tokens (from PDF text, chunk tags, or user input)
# Values are the matching sheet names (exact spelling matters for lookup)
# ---------------------------------------------------------------------------
_SHEET_NAMES = [
    "COVID-19",
    "Sepsis",
    "CAP",
    "CHF-ADHF",
    "NSTEMI-ACS",
    "AECOPD",
    "Pulmonary Embolism",
    "Ischemic Stroke",
]

_ALIASES: dict[str, list[str]] = {
    # COVID-19
    "covid":                ["COVID-19"],
    "covid-19":             ["COVID-19"],
    "covid19":              ["COVID-19"],
    "coronavirus":          ["COVID-19"],
    "sars-cov-2":           ["COVID-19"],

    # Sepsis
    "sepsis":               ["Sepsis"],
    "septic":               ["Sepsis"],
    "bacteremia":           ["Sepsis"],
    "septicemia":           ["Sepsis"],
    "systemic infection":   ["Sepsis"],

    # CAP — Community-Acquired Pneumonia
    "cap":                  ["CAP"],
    "pneumonia":            ["CAP"],
    "community-acquired":   ["CAP"],
    "lung infection":       ["CAP"],
    "lower respiratory":    ["CAP"],
    "pneumonitis":          ["CAP"],

    # CHF-ADHF
    "chf":                  ["CHF-ADHF"],
    "adhf":                 ["CHF-ADHF"],
    "heart failure":        ["CHF-ADHF"],
    "congestive":           ["CHF-ADHF"],
    "cardiac failure":      ["CHF-ADHF"],
    "decompensated heart":  ["CHF-ADHF"],
    "left ventricular":     ["CHF-ADHF"],
    "ejection fraction":    ["CHF-ADHF"],
    "chf-adhf":             ["CHF-ADHF"],

    # NSTEMI-ACS
    "nstemi":               ["NSTEMI-ACS"],
    "acs":                  ["NSTEMI-ACS"],
    "nstemi-acs":           ["NSTEMI-ACS"],
    "acute coronary":       ["NSTEMI-ACS"],
    "myocardial infarction":["NSTEMI-ACS"],
    "heart attack":         ["NSTEMI-ACS"],
    "unstable angina":      ["NSTEMI-ACS"],
    "troponin":             ["NSTEMI-ACS"],

    # AECOPD
    "aecopd":               ["AECOPD"],
    "copd":                 ["AECOPD"],
    "chronic obstructive":  ["AECOPD"],
    "exacerbation":         ["AECOPD"],
    "emphysema":            ["AECOPD"],
    "bronchitis":           ["AECOPD"],
    "obstructive pulmonary":["AECOPD"],

    # Pulmonary Embolism
    "pe":                   ["Pulmonary Embolism"],
    "pulmonary embolism":   ["Pulmonary Embolism"],
    "pulmonary embolus":    ["Pulmonary Embolism"],
    "dvt":                  ["Pulmonary Embolism"],
    "deep vein thrombosis": ["Pulmonary Embolism"],
    "blood clot":           ["Pulmonary Embolism"],
    "thromboembolism":      ["Pulmonary Embolism"],

    # Ischemic Stroke
    "stroke":               ["Ischemic Stroke"],
    "ischemic stroke":      ["Ischemic Stroke"],
    "cva":                  ["Ischemic Stroke"],
    "cerebrovascular":      ["Ischemic Stroke"],
    "tia":                  ["Ischemic Stroke"],
    "brain infarction":     ["Ischemic Stroke"],
    "ischemic":             ["Ischemic Stroke"],
}


def _resolve_sheets(query: str) -> list[str]:
    """
    Return the ordered list of sheet names to try for a given query string.

    Strategy (in priority order):
    1. Direct case-insensitive substring match against the known sheet list
    2. Alias look-up (exact key match on lower-cased query)
    3. Alias look-up (any alias key is a substring of the query, or vice-versa)
    """
    q = query.strip().lower()

    # 1 — direct substring
    direct = [s for s in _SHEET_NAMES if q in s.lower() or s.lower() in q]
    if direct:
        return direct

    # 2 — exact alias key
    if q in _ALIASES:
        return _ALIASES[q]

    # 3 — partial alias match (handles "Heart Failure" → "heart failure" key, etc.)
    for key, sheets in _ALIASES.items():
        if key in q or q in key:
            return sheets

    return []


def _filter_by_diagnosis(
    query: str,
    all_prompts: list[NursePrompt],
) -> list[NursePrompt]:
    """
    Filter prompts by diagnosis.  Falls back to all prompts when nothing matches.
    """
    if not query.strip():
        return all_prompts

    target_sheets = _resolve_sheets(query)
    if not target_sheets:
        return all_prompts          # unknown diagnosis → show everything

    matched = [
        p for p in all_prompts
        if (p.sheet_name or p.job_aid or "") in target_sheets
    ]
    return matched if matched else all_prompts


@router.get("/prompts", response_model=list[NursePrompt])
async def get_prompts(
    diagnosis: str | None = Query(
        default=None,
        description=(
            "Optional diagnosis keyword to filter prompts to a specific clinical sheet. "
            "Fuzzy-matched against known diagnoses; falls back to all prompts when "
            "no match is found."
        ),
    ),
    loader: NursePromptLoader = Depends(get_nurse_prompt_loader),
) -> list[NursePrompt]:
    all_prompts = loader.get_all()

    if not diagnosis:
        return all_prompts

    return _filter_by_diagnosis(diagnosis, all_prompts)
