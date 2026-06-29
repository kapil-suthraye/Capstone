from sample_data.claims_data import get_claim


def get_discrepancies(claim_id):

    patient = get_claim(claim_id)

    diagnosis = patient["Diagnosis"]

    return [

        {
            "Category": "Diagnosis",

            "Claim": diagnosis,

            "Medical Record": diagnosis,

            "Status": "Matched",

            "Severity": "Low",

            "Confidence": "99%"
        },

        {
            "Category": "Length of Stay",

            "Claim": "5 Days",

            "Medical Record": "4 Days",

            "Status": "Mismatch",

            "Severity": "Medium",

            "Confidence": "96%"
        },

        {
            "Category": "MRI Procedure",

            "Claim": "MRI Billed",

            "Medical Record": "No MRI Found",

            "Status": "Mismatch",

            "Severity": "High",

            "Confidence": "98%"
        }

    ]