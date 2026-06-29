import streamlit as st
import time


def ai_processing():

    progress = st.progress(0)

    status = st.empty()

    steps = [

        "Reading Medical Records",

        "Extracting Diagnoses",

        "Finding Supporting Evidence",

        "Comparing Billing Information",

        "Generating Clinical Summary"

    ]

    for i, step in enumerate(steps):

        status.info(step)

        progress.progress((i + 1) * 20)

        time.sleep(0.5)

    status.success("AI Analysis Completed")