import pandas as pd

def get_recent_claims():
    return pd.DataFrame({
        "Claim ID": ["CLM1001", "CLM1002", "CLM1003", "CLM1004"],
        "Patient": ["John Doe", "Alice Smith", "Robert Brown", "Emma Wilson"],
        "Diagnosis": ["Pneumonia", "Fracture", "Diabetes", "Hypertension"],
        "Priority": ["High", "Medium", "Low", "High"],
        "Status": ["Pending", "Completed", "Pending", "Review"]
    })

def get_claim_trend():
    return pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Claims":[320,410,390,470,520,490,610]
    })

def get_status_data():
    return pd.DataFrame({
        "Status":["Completed","Pending","Escalated"],
        "Count":[2806,218,45]
    })