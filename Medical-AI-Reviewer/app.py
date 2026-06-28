import streamlit as st

from config import *
from components.sidebar import load_sidebar
from views.dashboard import dashboard_page
from views.claims import claims_page
from views.claim_details import claim_details_page
from views.ai_review import ai_review_page
from views.evidence import evidence_page
from views.discrepancy import discrepancy_page
from views.recommendation import recommendation_page
from views.reports import report_page
from views.admin import admin_page

st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected = load_sidebar()

if selected == "Dashboard":
    dashboard_page()

elif selected == "Claims":
    claims_page()

elif selected == "Claim Details":
    claim_details_page()

elif selected == "AI Review":
    ai_review_page()

elif selected == "Evidence":
    evidence_page()

elif selected == "Discrepancy":
    discrepancy_page()

elif selected == "Recommendation":
    recommendation_page()

elif selected == "Reports":
    report_page()

elif selected == "Admin":
    admin_page()
