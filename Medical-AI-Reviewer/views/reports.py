import streamlit as st
import pandas as pd

from components.header import app_header
from sample_data.claims_data import get_claim


def report_page():

    app_header()

    claim = st.session_state.selected_claim

    patient = get_claim(claim)

    reviewer = st.session_state.get(
        "reviewer_name",
        "Reviewer"
    )

    decision = st.session_state.get(
        "final_decision",
        "Pending"
    )

    notes = st.session_state.get(
        "reviewer_notes",
        ""
    )

    st.subheader(f"📄 Claim Review Report - {claim}")

    st.divider()

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown("## Patient Information")

        st.write(f"**Claim ID:** {claim}")

        st.write(f"**Patient:** {patient['Patient']}")

        st.write(f"**Hospital:** {patient['Hospital']}")

        st.write(f"**Diagnosis:** {patient['Diagnosis']}")

        st.write(f"**Admission:** {patient['Admission']}")

        st.write(f"**Discharge:** {patient['Discharge']}")

    with col2:

        st.metric(
            "AI Score",
            f"{patient['AI Score']}%"
        )

        st.metric(
            "Priority",
            patient["Priority"]
        )

    st.divider()

    st.subheader("AI Findings")

    st.success("✔ Diagnosis Verified")

    st.success("✔ Clinical Documentation Available")

    st.success("✔ Medication Records Verified")

    st.error("✖ Billing Validation Requires Review")

    st.divider()

    st.subheader("Reviewer Decision")

    st.info(decision)

    st.divider()

    st.subheader("Reviewer Notes")

    if notes:

        st.write(notes)

    else:

        st.caption("No notes added.")

    st.divider()

    st.subheader("Audit Information")

    st.write(f"Reviewer : {reviewer}")

    st.write("Model : Medical AI Reviewer v1.0")

    st.write("Status : Completed")

    st.divider()

    report = pd.DataFrame({

        "Field":[

            "Claim ID",

            "Patient",

            "Diagnosis",

            "Hospital",

            "Priority",

            "AI Score",

            "Reviewer",

            "Decision"

        ],

        "Value":[

            claim,

            patient["Patient"],

            patient["Diagnosis"],

            patient["Hospital"],

            patient["Priority"],

            patient["AI Score"],

            reviewer,

            decision

        ]

    })

    csv = report.to_csv(index=False).encode()

    col1,col2 = st.columns(2)

    with col1:

        st.download_button(

            "⬇ Download CSV",

            csv,

            file_name=f"{claim}_Report.csv",

            mime="text/csv",

            use_container_width=True

        )

    with col2:

        st.download_button(

            "⬇ Download TXT Report",

            report.to_string(),

            file_name=f"{claim}_Report.txt",

            use_container_width=True

        )

    st.divider()

    if st.button(

        "🏠 Return to Dashboard",

        use_container_width=True

    ):

        st.session_state.selected_claim = None

        st.session_state.current_page = "Dashboard"

        st.rerun()