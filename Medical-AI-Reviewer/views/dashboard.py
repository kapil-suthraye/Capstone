import streamlit as st
import plotly.express as px
from components.header import app_header

from sample_data.dashboard_data import (
    get_recent_claims,
    get_claim_trend,
    get_status_data
)

def dashboard_page():

    app_header()

    st.caption("Decision Support System for Post Claim Review")

    st.markdown("---")

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Today's Claims","3024","+12%")
    col2.metric("Pending","218","-5")
    col3.metric("Completed","2806","+220")
    col4.metric("Avg Review","4.2 min","-0.4")

    st.markdown("---")

    left,right=st.columns([2,1])

    trend=get_claim_trend()

    fig1=px.line(
        trend,
        x="Day",
        y="Claims",
        markers=True,
        title="Claims Trend"
    )

    status=get_status_data()

    fig2=px.pie(
        status,
        values="Count",
        names="Status",
        title="Review Status"
    )

    with left:
        st.plotly_chart(fig1,use_container_width=True)

    with right:
        st.plotly_chart(fig2,use_container_width=True)

    st.markdown("---")

    st.subheader("Recent Claims")

    st.dataframe(
        get_recent_claims(),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Notifications")

    st.info("15 High Priority Claims require review.")

    st.warning("2 Claims have missing discharge summaries.")

    st.success("AI successfully processed 278 claims today.")