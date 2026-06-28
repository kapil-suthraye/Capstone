import streamlit as st
import pandas as pd

from components.header import app_header

from sample_data.recommendation_data import *

def recommendation_page():

    app_header()

    st.subheader("📋 Final AI Recommendation")

    rec = get_recommendation()

    c1,c2,c3 = st.columns(3)

    with c1:

        st.warning(rec["Recommendation"])

    with c2:

        st.metric(
            "Confidence",
            rec["Confidence"]
        )

    with c3:

        st.metric(
            "Risk Score",
            rec["Risk"]
        )

    st.divider()

    st.subheader("Review Summary")

    for item,status in get_summary():

        if status=="Verified":

            st.success(f"✔ {item}")

        else:

            st.error(f"✖ {item}")

    st.divider()

    st.subheader("Reviewer Notes")

    notes = st.text_area(
        "",
        height=150,
        placeholder="Enter review comments..."
    )

    st.divider()

    st.subheader("Reviewer Decision")

    decision = st.radio(

        "",

        [

            "Approve Claim",

            "Escalate for Physician Review",

            "Reject Claim"

        ]
    )

    st.divider()

    report = pd.DataFrame({

        "Section":[

            "Recommendation",

            "Confidence",

            "Risk Score",

            "Decision"

        ],

        "Value":[

            rec["Recommendation"],

            rec["Confidence"],

            rec["Risk"],

            decision

        ]

    })

    csv = report.to_csv(index=False).encode()

    c1,c2 = st.columns(2)

    with c1:

        st.download_button(

            "📄 Download CSV",

            csv,

            "Claim_Report.csv"

        )

    with c2:

        st.button("📑 Generate PDF")

    st.divider()

    st.subheader("Audit Trail")

    st.markdown("""

✅ AI Review Completed

⬇

👩 Nurse Validation

⬇

📄 Report Generated

⬇

✔ Claim Closed

""")