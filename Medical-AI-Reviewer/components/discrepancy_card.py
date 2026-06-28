import streamlit as st

def discrepancy_card(item):

    risk = item["Risk"]

    if risk == "High":
        st.error(f"🔴 {item['Title']}")

    elif risk == "Medium":
        st.warning(f"🟡 {item['Title']}")

    else:
        st.success(f"🟢 {item['Title']}")

    c1, c2 = st.columns(2)

    with c1:

        st.write("### Insurance Claim")

        st.write(item["Claim"])

    with c2:

        st.write("### Medical Record")

        st.write(item["Record"])

    c3, c4 = st.columns(2)

    with c3:

        st.metric("Confidence", item["Confidence"])

    with c4:

        st.write("### AI Recommendation")

        st.write(item["Recommendation"])

    st.button(
        "🔍 View Evidence",
        key=item["Title"]
    )

    st.divider()