import streamlit as st

from components.header import app_header


def recommendation_page():

    app_header()

    claim = st.session_state.selected_claim

    review = st.session_state.review_result

    st.subheader("AI Recommendation")

    st.success(review["recommendation"])

    # patient = data["patient"]

    # st.subheader(
    #     f"📋 Final Recommendation - {claim}"
    # )

    # st.divider()

    # col1, col2 = st.columns([2,1])

    # with col1:

    #     st.write(f"### 👤 {patient['Patient']}")

    #     st.write(f"Hospital : {patient['Hospital']}")

    #     st.write(f"Diagnosis : {patient['Diagnosis']}")

    # with col2:

    #     st.metric(
    #         "Confidence",
    #         data["confidence"]
    #     )

    #     st.metric(
    #         "Risk Score",
    #         data["risk"]
    #     )

    # st.divider()

    # st.warning(
    #     data["recommendation"]
    # )

    # st.divider()

    # st.subheader("Review Summary")

    # for item, status in review_summary():

    #     if status:

    #         st.success(f"✔ {item}")

    #     else:

    #         st.error(f"✖ {item}")

    # st.divider()

    # st.subheader("Reviewer Notes")

    # notes = st.text_area(

    #     "Enter Notes",

    #     height=120,

    #     placeholder="Add review comments..."

    # )

    # st.divider()

    # st.subheader("Reviewer Decision")

    # decision = st.radio(

    #     "",

    #     [

    #         "Approve Claim",

    #         "Escalate for Physician Review",

    #         "Reject Claim"

    #     ]

    # )

    # st.divider()

    # left, right = st.columns(2)

    # with left:

    #     if st.button(

    #         "⬅ Back",

    #         use_container_width=True

    #     ):

    #         st.session_state.current_page = "Discrepancy"

    #         st.rerun()

    # with right:

    #     if st.button(

    #         "📄 Generate Report",

    #         use_container_width=True

    #     ):

    #         st.session_state.final_decision = decision

    #         st.session_state.reviewer_notes = notes

    #         st.session_state.current_page = "Reports"

    #         st.rerun()