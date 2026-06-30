import streamlit as st

from config import *

# ---------- View Imports ----------
from views.login import login_page
from views.dashboard import dashboard_page
from views.claims import claims_page
from views.claim_details import claim_details_page
from views.ai_review import ai_review_page
from views.evidence import evidence_page
from views.discrepancy import discrepancy_page
from views.recommendation import recommendation_page
from views.reports import report_page

# ---------- Component ----------
from components.sidebar import load_sidebar

# ---------- Page Config ----------
st.set_page_config(
    page_title=APP_NAME,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

# ---------- Load CSS ----------
try:
    with open("styles/style.css") as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# ======================================================
# Session State Initialization
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "selected_claim" not in st.session_state:
    st.session_state.selected_claim = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "reviewer_name" not in st.session_state:
    st.session_state.reviewer_name = "Amy Wilson"

if "review_result" not in st.session_state:
    st.session_state.review_result = None

if "review_loaded" not in st.session_state:
    st.session_state.review_loaded = False

# ======================================================
# LOGIN
# ======================================================

if not st.session_state.logged_in:

    login_page()

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

selected = load_sidebar()

# If sidebar returns a page,
# update current page.

if selected:

    st.session_state.current_page = selected

page = st.session_state.current_page

# ======================================================
# ROUTING
# ======================================================

if page == "Dashboard":

    dashboard_page()

elif page == "Claims":

    claims_page()

elif page == "Claim Details":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")
        # st.error("⚠ No claim selected")
        # if st.button("📋 Go to Claims Queue"):

        #     st.session_state.current_page = "Claims"

        #     st.rerun()
    else:

        claim_details_page()

elif page == "AI Review":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")

    else:

        ai_review_page()

elif page == "Evidence":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")

    else:

        evidence_page()

elif page == "Discrepancy":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")

    else:

        discrepancy_page()

elif page == "Recommendation":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")

    else:

        recommendation_page()

elif page == "Reports":

    if st.session_state.selected_claim is None:

        st.warning("Please select a claim from Claims Queue.")

    else:

        report_page()

# ======================================================
# FOOTER
# ======================================================

# st.markdown("---")
