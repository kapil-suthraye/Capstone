import pandas as pd


def load_claims():

    data = [

        {
            "Claim ID": "CLM1001",
            "Patient": "John Doe",
            "Age": 45,
            "Gender": "Male",
            "Hospital": "City Hospital",
            "Diagnosis": "Pneumonia",
            "Priority": "High",
            "Status": "Pending",
            "Admission": "12-Jun-2026",
            "Discharge": "16-Jun-2026",
            "AI Score": 98
        },

        {
            "Claim ID": "CLM1002",
            "Patient": "Alice Smith",
            "Age": 60,
            "Gender": "Female",
            "Hospital": "Apollo Hospital",
            "Diagnosis": "Diabetes",
            "Priority": "Medium",
            "Status": "Review",
            "Admission": "20-Jun-2026",
            "Discharge": "23-Jun-2026",
            "AI Score": 95
        },

        {
            "Claim ID": "CLM1003",
            "Patient": "Robert Brown",
            "Age": 53,
            "Gender": "Male",
            "Hospital": "Fortis",
            "Diagnosis": "Fracture",
            "Priority": "Low",
            "Status": "Completed",
            "Admission": "08-Jun-2026",
            "Discharge": "10-Jun-2026",
            "AI Score": 92
        },

        {
            "Claim ID": "CLM1004",
            "Patient": "Emma Wilson",
            "Age": 37,
            "Gender": "Female",
            "Hospital": "Max Hospital",
            "Diagnosis": "Hypertension",
            "Priority": "High",
            "Status": "Pending",
            "Admission": "14-Jun-2026",
            "Discharge": "17-Jun-2026",
            "AI Score": 97
        }

    ]

    return pd.DataFrame(data)


# -------------------------------------------------
# Returns one selected claim
# -------------------------------------------------

def get_claim(claim_id):

    df = load_claims()

    row = df[df["Claim ID"] == claim_id]

    if len(row) == 0:

        return None

    return row.iloc[0].to_dict()