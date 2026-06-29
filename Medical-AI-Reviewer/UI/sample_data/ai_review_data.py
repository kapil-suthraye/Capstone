from sample_data.claims_data import get_claim


def get_ai_review(claim_id):

    patient = get_claim(claim_id)

    diagnosis = patient["Diagnosis"]

    return {

        "summary": f"""
Patient {patient['Patient']} was admitted to
{patient['Hospital']}.

Primary Diagnosis:
{diagnosis}

Treatment completed successfully.

Patient discharged in stable condition.

No life-threatening complications observed.
""",

        "confidence": patient["AI Score"],

        "findings": [

            "Diagnosis verified",

            "Admission & discharge dates verified",

            "Medication records available",

            "Billing documents available"

        ]

    }