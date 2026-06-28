import streamlit as st
import pandas as pd

from sample_data.claims_data import load_claims


def claims_page():

    st.title("📋 Claims Queue")

    st.caption("Review and manage incoming insurance claims")

    df = load_claims()

    st.markdown("---")

    c1,c2,c3=st.columns([2,1,1])

    with c1:
        search = st.text_input(
            "Search Patient / Claim",
            placeholder="Search..."
        )

    with c2:
        priority = st.selectbox(
            "Priority",
            ["All","High","Medium","Low"]
        )

    with c3:
        status = st.selectbox(
            "Status",
            ["All","Pending","Review","Completed"]
        )

    filtered=df.copy()

    if search:

        filtered=filtered[
            filtered["Patient"].str.contains(search,case=False)
            |
            filtered["Claim ID"].str.contains(search,case=False)
        ]

    if priority!="All":
        filtered=filtered[
            filtered["Priority"]==priority
        ]

    if status!="All":
        filtered=filtered[
            filtered["Status"]==status
        ]

    st.markdown("---")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.write(f"Showing **{len(filtered)}** Claims")

    st.markdown("---")

    st.success("Select a claim from the list to begin AI Review.")