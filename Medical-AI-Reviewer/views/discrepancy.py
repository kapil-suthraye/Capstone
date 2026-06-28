import streamlit as st

from components.header import app_header
from components.discrepancy_card import discrepancy_card

from sample_data.discrepancy_data import get_discrepancies


def discrepancy_page():

    app_header()

    st.subheader("⚠ AI Discrepancy Detection")

    st.metric(
        "Overall AI Risk Score",
        "92%",
        "High Risk"
    )

    st.progress(92)

    st.divider()

    st.subheader("Detected Discrepancies")

    data = get_discrepancies()

    for item in data:

        discrepancy_card(item)

    st.divider()

    high = len([d for d in data if d["Risk"] == "High"])
    medium = len([d for d in data if d["Risk"] == "Medium"])
    low = len([d for d in data if d["Risk"] == "Low"])

    c1, c2, c3 = st.columns(3)

    c1.metric("🔴 High", high)
    c2.metric("🟡 Medium", medium)
    c3.metric("🟢 Low", low)

    st.divider()

    st.subheader("Reviewer Decision")

    b1, b2, b3 = st.columns(3)

    with b1:
        st.button("✅ Approve")

    with b2:
        st.button("📤 Escalate")

    with b3:
        st.button("❌ Reject")