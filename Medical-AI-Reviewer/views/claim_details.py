import streamlit as st

from sample_data.patient_data import get_patient
from sample_data.patient_data import get_documents

from components.header import app_header
from components.timeline import treatment_timeline


def claim_details_page():

    app_header()

    st.subheader("Claim Details")

    patient=get_patient()

    left,right=st.columns([2,1])

    with left:

        st.markdown("### 👤 Patient Information")

        st.write(f"**Claim ID:** {patient['Claim ID']}")
        st.write(f"**Patient:** {patient['Patient']}")
        st.write(f"**Age:** {patient['Age']}")
        st.write(f"**Gender:** {patient['Gender']}")
        st.write(f"**Hospital:** {patient['Hospital']}")
        st.write(f"**Diagnosis:** {patient['Diagnosis']}")
        st.write(
            f"**Stay:** {patient['Admission']} → {patient['Discharge']}"
        )

    with right:

        st.info("Priority : HIGH")

        st.metric(
            "AI Confidence",
            "98%"
        )

    st.divider()

    st.markdown("### 📂 Uploaded Documents")

    for doc in get_documents():

        st.success(f"✔ {doc}")

    st.divider()

    treatment_timeline()

    st.divider()

    if st.button("🤖 Analyze with AI"):

        st.success("Opening AI Review...")