from __future__ import annotations

import streamlit as st


PAGES = [
    "Executive Dashboard",
    "Health Score Engine",
    "Financial Intelligence",
    "Risk Intelligence",
    "Competitor Intelligence",
    "Strategy Command Center",
    "M&A Scanner",
    "Valuation Engine",
    "Forecasting Lab",
    "Board Pack PDF Generator",
    "AI Copilot",
]


def navigation() -> str:
    st.sidebar.title("Command Center")
    st.sidebar.caption("MBA portfolio edition")
    return st.sidebar.radio("Navigate", PAGES)

