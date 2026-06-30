import streamlit as st

from components.header import app_header
from components.discrepancy_card import discrepancy_card

from sample_data.discrepancy_data import get_discrepancies


def discrepancy_page():

    app_header()

    review = st.session_state.review_result

    missing = review["missing_documentation"]

    st.subheader("Missing Documentation")

    for item in missing:

        st.warning(item)

        
#     claim = st.session_state.selected_claim

#     st.subheader(
#         f"⚠ Discrepancy Detection - {claim}"
#     )

#     st.divider()

#     discrepancies = get_discrepancies(claim)

#     total = len(discrepancies)

#     mismatch = len(

#         [

#             d for d in discrepancies

#             if d["Status"] == "Mismatch"

#         ]

#     )

#     matched = total - mismatch

#     c1, c2, c3 = st.columns(3)

#     with c1:

#         st.metric(
#             "Total Checks",
#             total
#         )

#     with c2:

#         st.metric(
#             "Matched",
#             matched
#         )

#     with c3:

#         st.metric(
#             "Mismatches",
#             mismatch
#         )

#     st.divider()

#     st.subheader("Comparison")

#     for item in discrepancies:

#         discrepancy_card(item)

#         st.divider()

#     st.subheader("Overall Assessment")

#     st.warning("""

# Two discrepancies require manual validation.

# MRI billing could not be verified.

# Length of stay differs by one day.

# Recommendation:

# Proceed for Manual Review.

# """)

#     st.divider()

#     left, right = st.columns(2)

#     with left:

#         if st.button(

#             "⬅ Evidence",

#             use_container_width=True

#         ):

#             st.session_state.current_page = "Evidence"

#             st.rerun()

#     with right:

#         if st.button(

#             "Continue",

#             use_container_width=True

#         ):

#             st.session_state.current_page = "Recommendation"

#             st.rerun()