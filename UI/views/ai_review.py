import streamlit as st

from components.header import app_header
from components.processing import ai_processing

# from sample_data.ai_review_data import get_ai_review
from services.api import review_claim


def ai_review_page():

    app_header()

    claim = st.session_state.selected_claim

    if not st.session_state.review_loaded:

        payload = {

            "claim_id": claim,

            "document_path": f"documents/{claim}.pdf"

        }

        with st.spinner("Running Medical AI Review..."):

            review = review_claim(payload)

            st.session_state.review_result = review

            st.session_state.review_loaded = True

    else:

        review = st.session_state.review_result

    st.subheader(f"🤖 AI Review - {claim}")

    st.divider()

    ai_processing()

    st.divider()

    st.subheader("Clinical Summary")

    st.success(review["summary"])

    st.metric(

        "AI Confidence",

        f"{review['confidence']*100:.0f}%"

    )

    st.divider()

    st.subheader("Evidence")

    for item in review['evidence']:

        with st.container():

            st.markdown(f"### 📌 {item['finding']}")

            col1,col2 = st.columns(2)

            with col1:
                st.info(f"Source : {item['source']}")

            with col2:
                st.info(f"Page : {item['page']}")

            st.divider()

    # c1, c2 = st.columns(2)

    # with c1:

    #     if st.button(

    #         "⬅ Claim Details",

    #         use_container_width=True

    #     ):

    #         st.session_state.current_page = "Claim Details"

    #         st.rerun()

    # with c2:

    #     if st.button(

    #         "📄 View Evidence",

    #         use_container_width=True

    #     ):

    #         st.session_state.current_page = "Evidence"

    #         st.rerun()