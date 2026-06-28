def get_summary():

    return """
Patient admitted with Pneumonia.

Treatment included:

• IV Antibiotics

• Chest X-Ray

• Blood Tests

Patient responded well to treatment and was discharged in stable condition.
"""


def get_evidence():

    return [

        {
            "title":"Diagnosis",
            "page":12,
            "text":"Pneumonia confirmed by Chest X-Ray.",
            "confidence":"98%"
        },

        {
            "title":"Medication",
            "page":34,
            "text":"IV Ceftriaxone administered.",
            "confidence":"97%"
        },

        {
            "title":"Procedure",
            "page":48,
            "text":"Chest X-Ray performed.",
            "confidence":"99%"
        }

    ]


def get_discrepancies():

    return [

        {
            "Claim":"MRI Scan",
            "Record":"No MRI found",
            "Severity":"High"
        },

        {
            "Claim":"Length of Stay = 5 Days",
            "Record":"Actual Stay = 4 Days",
            "Severity":"Medium"
        }

    ]