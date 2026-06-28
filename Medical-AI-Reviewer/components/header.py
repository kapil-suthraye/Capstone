import streamlit as st

def app_header():

    left, middle, right = st.columns([6,2,2])

    with left:
        st.title("🏥 Medical AI Reviewer")
        st.caption("AI Decision Support for Insurance Claim Validation")

    with middle:
        st.write("")
        st.info("📅 28 June 2026")

    with right:
        st.write("")
        st.success("👩 Nurse Reviewer")