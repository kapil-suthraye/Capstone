import streamlit as st

from components.header import app_header
from components.evidence_card import evidence_card

from sample_data.evidence_data import *

def evidence_page():

    app_header()

    st.subheader("📄 Evidence Viewer")

    search = st.text_input(
        "Search Medical Record"
    )

    st.divider()

    st.markdown("### 🩺 Patient Timeline")

    st.progress(100)

    st.write(
        "Admission → Diagnosis → Medication → Lab → Discharge"
    )

    st.divider()

    st.markdown("### Supporting Evidence")

    for evidence in get_evidence():

        if search:

            if search.lower() not in evidence["Evidence"].lower():

                continue

        evidence_card(evidence)

    st.divider()

    st.markdown("### 🤖 AI Explanation")

    st.info(ai_explanation())

    st.divider()

    st.markdown("### 💬 Ask Medical AI")

    if "messages" not in st.session_state:

        st.session_state.messages=[]

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.write(msg["content"])

    prompt=st.chat_input(
        "Ask about this claim..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message("user"):

            st.write(prompt)

        answer="""
The AI searched every uploaded medical record.

No MRI report was found.

The billed MRI could not be validated.

Recommendation:
Manual Review.
"""

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

        with st.chat_message("assistant"):

            st.write(answer)