import pandas as pd

def load_claims():

    return pd.DataFrame({

        "Claim ID":[
            "CLM1001",
            "CLM1002",
            "CLM1003",
            "CLM1004",
            "CLM1005",
            "CLM1006"
        ],

        "Patient":[
            "John Doe",
            "Alice Smith",
            "Robert Brown",
            "Emma Wilson",
            "James Miller",
            "Sophia Davis"
        ],

        "Hospital":[
            "City Hospital",
            "Apollo",
            "Fortis",
            "Max",
            "Aster",
            "Medanta"
        ],

        "Diagnosis":[
            "Pneumonia",
            "Diabetes",
            "Fracture",
            "Hypertension",
            "Asthma",
            "Stroke"
        ],

        "Priority":[
            "High",
            "Medium",
            "Low",
            "High",
            "Medium",
            "High"
        ],

        "Status":[
            "Pending",
            "Completed",
            "Review",
            "Pending",
            "Completed",
            "Review"
        ],

        "AI Score":[
            98,
            95,
            92,
            97,
            90,
            99
        ]
    })