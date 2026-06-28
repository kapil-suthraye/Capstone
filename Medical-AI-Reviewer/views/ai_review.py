import streamlit as st

from components.header import app_header
from components.progress import ai_processing

from sample_data.ai_review_data import *

def ai_review_page():

    app_header()

    st.subheader("🤖 AI Medical Review")

    ai_processing()

    st.divider()

    st.subheader("📝 AI Generated Summary")

    st.success(get_summary())

    st.divider()

    st.subheader("📄 Supporting Evidence")

    for evidence in get_evidence():

        with st.expander(
            f"{evidence['title']}  |  Page {evidence['page']}"
        ):

            st.write(evidence["text"])

            st.metric(
                "Confidence",
                evidence["confidence"]
            )

    st.divider()

    st.subheader("⚠ Detected Discrepancies")

    for d in get_discrepancies():

        st.error(
            f"""
Claim

{d['Claim']}

Medical Record

{d['Record']}

Severity

{d['Severity']}
"""
        )

    st.divider()

    c1,c2,c3=st.columns(3)

    with c1:
        st.button("🔍 View Evidence")

    with c2:
        st.button("📄 Generate Report")

    with c3:
        st.button("➡ Continue")