import streamlit as st
from streamlit_option_menu import option_menu

def load_sidebar():

    with st.sidebar:

        st.title("🩺 Medical AI")

        st.markdown("---")

        selected = option_menu(
            menu_title="Navigation",
            options=[
                "Dashboard",
                "Claims",
                "Claim Details",
                "AI Review",
                "Evidence",
                "Discrepancy",
                "Recommendation",
                "Reports",
                "Admin"
            ],
            icons=[
                "speedometer2",
                "file-earmark-medical",
                "person-badge",
                "robot",
                "search",
                "exclamation-circle",
                "clipboard-check",
                "file-earmark-pdf",
                "gear"
            ],
            default_index=0,
        )

    return selected