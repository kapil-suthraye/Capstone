import streamlit as st

from sample_data.claims_data import load_claims


def claims_page():

    st.title("📋 Claims Queue")

    st.caption("Review incoming medical insurance claims")

    df = load_claims()

    search = st.text_input(
        "Search Claim / Patient"
    )

    if search:

        df = df[
            df["Patient"].str.contains(
                search,
                case=False
            )
            |
            df["Claim ID"].str.contains(
                search,
                case=False
            )
        ]

    st.divider()

    for _, row in df.iterrows():

        with st.container(border=True):

            left, right = st.columns([4, 1])

            with left:

                st.subheader(row["Claim ID"])

                st.write(f"👤 {row['Patient']}")

                st.write(f"🏥 {row['Hospital']}")

                st.write(f"🩺 {row['Diagnosis']}")

                st.write(
                    f"Priority : {row['Priority']}"
                )

                st.write(
                    f"Status : {row['Status']}"
                )

            with right:

                st.metric(
                    "AI Score",
                    f"{row['AI Score']}%"
                )

                if st.button(
                    "Review",
                    key=row["Claim ID"]
                ):

                    st.session_state.selected_claim = row["Claim ID"]

                    st.session_state.current_page = "Claim Details"

                    st.success(
                        f"Selected {row['Claim ID']}"
                    )

                    st.rerun()