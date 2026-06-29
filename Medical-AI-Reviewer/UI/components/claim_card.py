import streamlit as st

from components.badges import priority_badge
from components.badges import status_badge

def claim_card(row):

    left,right=st.columns([5,1])

    with left:

        st.markdown(f"### {row['Claim ID']}")

        st.write(f"👤 **Patient:** {row['Patient']}")

        st.write(f"🏥 **Hospital:** {row['Hospital']}")

        st.write(f"🩺 **Diagnosis:** {row['Diagnosis']}")

        st.write(f"Priority: {priority_badge(row['Priority'])}")

        st.write(f"Status: {status_badge(row['Status'])}")

    with right:

        st.metric(
            "AI Score",
            f"{row['AI Score']}%"
        )

        st.button(
            "Review",
            key=row["Claim ID"]
        )

    st.divider()