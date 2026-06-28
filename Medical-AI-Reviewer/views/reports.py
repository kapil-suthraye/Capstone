import streamlit as st

from components.header import app_header

def report_page():

    app_header()

    st.subheader("📄 Claim Review Report")

    st.success("Report Generated Successfully")

    st.markdown("""

### Executive Summary

Claim Number : CLM1001

Patient : John Doe

Diagnosis : Pneumonia

Recommendation : Manual Review

Confidence : 96%

----------------------------------

### AI Findings

✔ Diagnosis Verified

✔ Medication Verified

✔ Treatment Timeline Verified

✖ MRI Procedure Missing

----------------------------------

### Reviewer Decision

Pending

""")

    st.download_button(

        "Download Report",

        "Demo Report",

        "Medical_AI_Report.txt"

    )