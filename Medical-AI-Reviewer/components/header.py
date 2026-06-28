import streamlit as st

def app_header():

    left, right = st.columns([5,1])

    with left:
        st.title("🏥 Medical AI Reviewer")
        st.caption("AI Decision Support for Insurance Claim Review")

    with right:
        st.markdown("### 👤")
        st.write("Nurse Reviewer")