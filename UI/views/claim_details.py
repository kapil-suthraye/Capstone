import streamlit as st

from components.header import app_header
from components.timeline import treatment_timeline

# from sample_data.patient_data import (
#     get_patient,
#     get_documents
# )


def claim_details_page():

    app_header()

    review = st.session_state.review_result

    # claim_id = st.session_state.selected_claim

    # patient = get_patient(claim_id)

    # st.subheader(f"📄 Claim Details - {claim_id}")

    # st.divider()

    # left, right = st.columns([2,1])

    # with left:

    #     st.markdown("## 👤 Patient Information")

    #     st.write(f"**Patient:** {patient['Patient']}")

    #     st.write(f"**Age:** {patient['Age']}")

    #     st.write(f"**Gender:** {patient['Gender']}")

    #     st.write(f"**Hospital:** {patient['Hospital']}")

    #     st.write(f"**Diagnosis:** {patient['Diagnosis']}")

    #     st.write(
    #         f"**Admission:** {patient['Admission']}"
    #     )

    #     st.write(
    #         f"**Discharge:** {patient['Discharge']}"
    #     )

    # with right:

    #     st.metric(
    #         "AI Confidence",
    #         f"{patient['AI Score']}%"
    #     )

    #     st.info(
    #         f"Priority : {patient['Priority']}"
    #     )

    #     st.success(
    #         f"Status : {patient['Status']}"
    #     )

    # st.divider()

    # st.markdown("## 📂 Uploaded Documents")

    # docs = get_documents(claim_id)

    # for doc in docs:

    #     st.success(f"✔ {doc}")

    # st.divider()

    # treatment_timeline()

    # st.divider()

    # col1,col2 = st.columns(2)

    # with col1:

    #     if st.button(
    #         "⬅ Back to Claims",
    #         use_container_width=True
    #     ):

    #         st.session_state.current_page = "Claims"

    #         st.rerun()

    # with col2:

    #     if st.button(
    #         "🤖 Analyze with AI",
    #         use_container_width=True
    #     ):

    #         st.session_state.current_page = "AI Review"

    #         st.rerun()