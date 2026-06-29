import streamlit as st

from components.header import app_header
from components.evidence_card import evidence_card

from sample_data.evidence_data import (
    get_evidence,
    get_ai_explanation
)


def evidence_page():

    app_header()

    claim = st.session_state.selected_claim

    st.subheader(f"📄 Evidence Viewer - {claim}")

    st.divider()

    search = st.text_input(
        "Search Medical Record"
    )

    st.divider()

    st.subheader("🩺 Treatment Timeline")

    st.progress(100)

    st.write(
        "Admission → Diagnosis → Medication → Laboratory → Discharge"
    )

    st.divider()

    st.subheader("Supporting Evidence")

    evidence = get_evidence(claim)

    for item in evidence:

        if search:

            if search.lower() not in item["Evidence"].lower():

                continue

        evidence_card(item)

    st.divider()

    st.subheader("🤖 AI Explanation")

    st.info(
        get_ai_explanation(claim)
    )

    st.divider()

    st.subheader("💬 Ask Medical AI")

    if "chat" not in st.session_state:

        st.session_state.chat = []

    for msg in st.session_state.chat:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

    prompt = st.chat_input(
        "Ask about this claim..."
    )

    if prompt:

        st.session_state.chat.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message("user"):

            st.write(prompt)

        answer = """
The diagnosis is well supported by
clinical documentation.

One billing discrepancy was identified.

Please continue to the Discrepancy page
for detailed validation.
"""

        st.session_state.chat.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

        with st.chat_message("assistant"):

            st.write(answer)

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ AI Review",
            use_container_width=True
        ):

            st.session_state.current_page = "AI Review"

            st.rerun()

    with col2:

        if st.button(
            "⚠ View Discrepancies",
            use_container_width=True
        ):

            st.session_state.current_page = "Discrepancy"

            st.rerun()