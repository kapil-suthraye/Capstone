import streamlit as st

def metric_card(title, value, delta):

    st.metric(
        label=title,
        value=value,
        delta=delta
    )