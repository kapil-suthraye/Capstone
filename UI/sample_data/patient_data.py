from sample_data.claims_data import get_claim


DOCUMENTS = {

    "CLM1001": [
        "Discharge Summary.pdf",
        "Physician Notes.pdf",
        "Lab Reports.pdf",
        "Billing Statement.pdf"
    ],

    "CLM1002": [
        "Diabetes Assessment.pdf",
        "Medication Chart.pdf",
        "Blood Report.pdf",
        "Invoice.pdf"
    ],

    "CLM1003": [
        "Orthopedic Notes.pdf",
        "X-Ray Report.pdf",
        "Discharge Summary.pdf"
    ],

    "CLM1004": [
        "Admission Notes.pdf",
        "Blood Pressure Chart.pdf",
        "ECG Report.pdf",
        "Discharge Summary.pdf"
    ]

}


def get_patient(claim_id):

    return get_claim(claim_id)


def get_documents(claim_id):

    return DOCUMENTS.get(claim_id, [])