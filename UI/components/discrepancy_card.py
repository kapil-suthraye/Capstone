import streamlit as st


def discrepancy_card(item):

    with st.container(border=True):

        st.subheader(item["Category"])

        left, right = st.columns(2)

        with left:

            st.write("### Insurance Claim")

            st.info(item["Claim"])

        with right:

            st.write("### Medical Record")

            st.info(item["Medical Record"])

        c1, c2, c3 = st.columns(3)

        with c1:

            if item["Status"] == "Matched":

                st.success("Matched")

            else:

                st.error("Mismatch")

        with c2:

            if item["Severity"] == "High":

                st.error("High")

            elif item["Severity"] == "Medium":

                st.warning("Medium")

            else:

                st.success("Low")

        with c3:

            st.metric(
                "Confidence",
                item["Confidence"]
            )