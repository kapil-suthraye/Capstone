"""
Generate synthetic medical-record PDFs for upload load tests.

Why: never load-test with real patient PDFs. This produces structured,
multi-section documents (headings, meds, labs) so the parser/chunker in the
Capstone backend has realistic work to do — diagnoses, medications, and lab
values that its clinical-aware chunker will tag.

Usage:
    python generate_test_pdf.py                # 1 PDF, 6 pages
    python generate_test_pdf.py --count 5 --pages 12
"""

import argparse
import os
import random

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

DIAGNOSES = [
    "Community-acquired pneumonia", "Congestive heart failure exacerbation",
    "Type 2 diabetes mellitus with hyperglycemia", "Acute kidney injury",
    "COPD exacerbation", "Cellulitis of the lower extremity",
    "Atrial fibrillation with rapid ventricular response",
]
MEDICATIONS = [
    "Ceftriaxone 1g IV q24h", "Azithromycin 500mg PO daily",
    "Furosemide 40mg IV BID", "Metformin 1000mg PO BID",
    "Insulin glargine 20 units SC nightly", "Albuterol nebulizer q4h PRN",
    "Apixaban 5mg PO BID", "Vancomycin 1.25g IV q12h",
]
LABS = [
    ("WBC", "13.4", "x10^3/uL"), ("Hemoglobin", "10.8", "g/dL"),
    ("Creatinine", "1.9", "mg/dL"), ("BUN", "34", "mg/dL"),
    ("Glucose", "212", "mg/dL"), ("BNP", "890", "pg/mL"),
    ("Lactate", "2.1", "mmol/L"), ("Potassium", "3.4", "mEq/L"),
]
SECTIONS = [
    "CHIEF COMPLAINT", "HISTORY OF PRESENT ILLNESS", "PAST MEDICAL HISTORY",
    "MEDICATIONS", "PHYSICAL EXAMINATION", "LABORATORY RESULTS",
    "ASSESSMENT AND PLAN", "PROGRESS NOTE",
]
FILLER = (
    "Patient remains hemodynamically stable. Continues on current regimen "
    "with gradual clinical improvement noted on serial examination. "
    "Oxygen requirements decreasing. Tolerating oral intake. "
    "Ambulating with physical therapy assistance. "
)


def write_pdf(path: str, pages: int, seed: int) -> None:
    rng = random.Random(seed)
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter

    for page in range(pages):
        y = height - 0.75 * inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(0.75 * inch, y, f"SYNTHETIC MEDICAL RECORD — Page {page + 1}")
        y -= 0.4 * inch

        for _ in range(3):
            section = rng.choice(SECTIONS)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(0.75 * inch, y, section)
            y -= 0.25 * inch
            c.setFont("Helvetica", 10)

            if section == "MEDICATIONS":
                for med in rng.sample(MEDICATIONS, 4):
                    c.drawString(1.0 * inch, y, f"- {med}")
                    y -= 0.2 * inch
            elif section == "LABORATORY RESULTS":
                for name, val, unit in rng.sample(LABS, 5):
                    c.drawString(1.0 * inch, y, f"{name}: {val} {unit}")
                    y -= 0.2 * inch
            else:
                dx = rng.choice(DIAGNOSES)
                text = f"Primary diagnosis: {dx}. " + FILLER * rng.randint(2, 4)
                # naive wrap at ~95 chars
                while text:
                    line, text = text[:95], text[95:]
                    c.drawString(1.0 * inch, y, line)
                    y -= 0.18 * inch
                    if y < 1 * inch:
                        break
            y -= 0.25 * inch
            if y < 1.5 * inch:
                break
        c.showPage()
    c.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--pages", type=int, default=6)
    ap.add_argument("--outdir", default="test_records")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    for i in range(args.count):
        name = "synthetic_record.pdf" if args.count == 1 else f"synthetic_record_{i+1}.pdf"
        path = os.path.join(args.outdir, name)
        write_pdf(path, args.pages, seed=i)
        print(f"wrote {path} ({args.pages} pages)")


if __name__ == "__main__":
    main()
