import streamlit as st

from components.header import app_header
from components.processing import ai_processing

from sample_data.ai_review_data import get_ai_review


def ai_review_page():

    app_header()

    claim = st.session_state.selected_claim

    review = get_ai_review(claim)

    st.subheader(f"🤖 AI Review - {claim}")

    st.divider()

    ai_processing()

    st.divider()

    st.subheader("Clinical Summary")

    st.success(review["summary"])

    st.metric(

        "AI Confidence",

        f"{review['confidence']}%"

    )

    st.divider()

    st.subheader("Key Findings")

    for item in review["findings"]:

        st.success(f"✔ {item}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(

            "⬅ Claim Details",

            use_container_width=True

        ):

            st.session_state.current_page = "Claim Details"

            st.rerun()

    with c2:

        if st.button(

            "📄 View Evidence",

            use_container_width=True

        ):

            st.session_state.current_page = "Evidence"

            st.rerun()