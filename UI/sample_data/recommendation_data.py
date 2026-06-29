from sample_data.claims_data import get_claim


def get_recommendation(claim_id):

    patient = get_claim(claim_id)

    if patient["Priority"] == "High":

        recommendation = "Requires Manual Review"

        confidence = "96%"

        risk = "92%"

    elif patient["Priority"] == "Medium":

        recommendation = "Review Recommended"

        confidence = "94%"

        risk = "70%"

    else:

        recommendation = "Suitable for Approval"

        confidence = "98%"

        risk = "25%"

    return {

        "patient": patient,

        "recommendation": recommendation,

        "confidence": confidence,

        "risk": risk

    }


def review_summary():

    return [

        ("Diagnosis", True),

        ("Clinical Notes", True),

        ("Medication", True),

        ("Billing Validation", False)

    ]