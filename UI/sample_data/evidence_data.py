from sample_data.claims_data import get_claim


def get_evidence(claim_id):

    patient = get_claim(claim_id)

    diagnosis = patient["Diagnosis"]

    return [

        {
            "Category": "Diagnosis",
            "Page": 12,
            "Confidence": "98%",
            "Evidence":
                f"Primary diagnosis confirmed as {diagnosis}."
        },

        {
            "Category": "Medication",
            "Page": 25,
            "Confidence": "96%",
            "Evidence":
                "Medication administration record verified."
        },

        {
            "Category": "Laboratory",
            "Page": 42,
            "Confidence": "99%",
            "Evidence":
                "Lab investigations support the diagnosis."
        },

        {
            "Category": "Discharge Summary",
            "Page": 58,
            "Confidence": "97%",
            "Evidence":
                "Patient discharged in stable condition."
        }

    ]


def get_ai_explanation(claim_id):

    patient = get_claim(claim_id)

    return f"""
The AI reviewed all uploaded medical documents for
{patient['Patient']}.

Clinical evidence consistently supports the diagnosis.

However, billing records contain one or more items that
require manual validation.

Recommendation:

Proceed to Discrepancy Review.
"""