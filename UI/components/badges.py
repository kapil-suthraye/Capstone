import streamlit as st

def priority_badge(priority):

    colors = {
        "High":"🔴 High",
        "Medium":"🟡 Medium",
        "Low":"🟢 Low"
    }

    return colors.get(priority,"⚪ Unknown")


def status_badge(status):

    colors = {
        "Pending":"🟠 Pending",
        "Completed":"🟢 Completed",
        "Review":"🔵 Review"
    }

    return colors.get(status,status)