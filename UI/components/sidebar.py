import streamlit as st
from streamlit_option_menu import option_menu


def load_sidebar():

    with st.sidebar:

        # ==========================================
        # Logo
        # ==========================================

        st.markdown("# 🏥 Medical AI")

        st.caption("Reviewer Portal")

        st.divider()

        # ==========================================
        # User Information
        # ==========================================

        reviewer = st.session_state.get(
            "reviewer_name",
            "Reviewer"
        )

        role = st.session_state.get(
            "role",
            "Nurse"
        )

        st.markdown(f"### 👤 {reviewer}")

        st.caption(role)

        st.divider()

        # ==========================================
        # Navigation
        # ==========================================

        selected = option_menu(
            menu_title=None,

            options=[
                "Dashboard",
                "Claims",
                "Claim Details",
                "AI Review",
                "Evidence",
                "Discrepancy",
                "Recommendation",
                "Reports"
            ],

            icons=[
                "house",
                "clipboard-data",
                "person-badge",
                "robot",
                "file-earmark-text",
                "exclamation-triangle",
                "clipboard-check",
                "file-earmark-pdf"
            ],

            default_index=0
        )

        st.divider()

        # ==========================================
        # Selected Claim
        # ==========================================

        if st.session_state.selected_claim:

            st.success(
                f"Selected Claim\n\n{st.session_state.selected_claim}"
            )

        else:

            st.info("No Claim Selected")

        st.divider()

        # ==========================================
        # Logout
        # ==========================================

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.selected_claim = None

            st.session_state.current_page = "Dashboard"

            st.rerun()

        st.divider()

    return selected