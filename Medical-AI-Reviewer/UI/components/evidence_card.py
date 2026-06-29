import streamlit as st


def evidence_card(item):

    with st.container(border=True):

        left, right = st.columns([4,1])

        with left:

            st.subheader(item["Category"])

            st.write(item["Evidence"])

            st.caption(f"📄 Page {item['Page']}")

        with right:

            st.metric(
                "Confidence",
                item["Confidence"]
            )