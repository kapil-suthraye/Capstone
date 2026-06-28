def get_evidence():

    return [

        {
            "Category":"Diagnosis",

            "Page":"12",

            "Confidence":"98%",

            "Evidence":"Chest X-Ray confirms Pneumonia."
        },

        {
            "Category":"Medication",

            "Page":"34",

            "Confidence":"97%",

            "Evidence":"IV Ceftriaxone administered."
        },

        {
            "Category":"Lab Result",

            "Page":"51",

            "Confidence":"99%",

            "Evidence":"Elevated White Blood Cell Count."
        }

    ]


def ai_explanation():

    return """
MRI was billed in the insurance claim.

The AI searched all uploaded medical records.

No MRI order, report or imaging evidence was found.

Therefore the claim was flagged for manual review.
"""