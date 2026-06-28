import pandas as pd

def get_patient():

    return {

        "Claim ID":"CLM1001",

        "Patient":"John Doe",

        "Age":45,

        "Gender":"Male",

        "Hospital":"City Hospital",

        "Diagnosis":"Pneumonia",

        "Admission":"12-Jun-2026",

        "Discharge":"16-Jun-2026"

    }


def get_documents():

    return [

        "Discharge Summary.pdf",

        "Physician Notes.pdf",

        "Lab Reports.pdf",

        "Billing Statement.pdf"

    ]