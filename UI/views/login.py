import streamlit as st


def login_page():

    # -------------------------
    # Center the Login Form
    # -------------------------

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style='text-align:center'>
                <h1>🏥 Medical AI Reviewer</h1>
                <p style='font-size:18px;color:gray'>
                AI Assisted Post Claim Review
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        username = st.text_input(
            "Username",
            placeholder="Enter Username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        remember = st.checkbox("Remember Me")

        st.write("")

        if st.button(
            "Login",
            use_container_width=True
        ):

            users = {

                "nurse": {
                    "password": "ey123",
                    "name": "Amy Wilson",
                    "role": "Nurse Reviewer"
                },

                "manager": {
                    "password": "ey123",
                    "name": "David Smith",
                    "role": "Review Manager"
                }

            }

            if username in users:

                if password == users[username]["password"]:

                    st.session_state.logged_in = True

                    st.session_state.reviewer_name = users[
                        username
                    ]["name"]

                    st.session_state.role = users[
                        username
                    ]["role"]

                    st.success("Login Successful")

                    st.rerun()

            st.error("Invalid Username or Password")

        st.markdown("---")

        st.caption("Demo Credentials")

        st.code(
            """
Username : nurse
Password : ey123

OR

Username : manager
Password : ey123
"""
        )
