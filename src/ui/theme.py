from __future__ import annotations

import streamlit as st

from src.config import ACCENT, INK, PAPER, PRIMARY


def apply_theme() -> None:
    st.set_page_config(
        page_title="MBA Strategy Command Center",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        f"""
        <style>
        :root {{
          --primary: {PRIMARY};
          --accent: {ACCENT};
          --ink: {INK};
          --paper: {PAPER};
        }}
        .main .block-container {{
          padding-top: 1.25rem;
          padding-bottom: 2rem;
        }}
        h1, h2, h3 {{
          color: var(--ink);
          letter-spacing: 0;
        }}
        div[data-testid="stMetric"] {{
          background: #ffffff;
          border: 1px solid #e6e8ec;
          border-radius: 8px;
          padding: 1rem;
          box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
        }}
        .insight-box {{
          background: #ffffff;
          border-left: 4px solid var(--primary);
          border-radius: 8px;
          padding: 0.9rem 1rem;
          border-top: 1px solid #e6e8ec;
          border-right: 1px solid #e6e8ec;
          border-bottom: 1px solid #e6e8ec;
          margin: 0.35rem 0;
        }}
        .risk-high {{ color: #c73e1d; font-weight: 700; }}
        .risk-medium {{ color: #a15c00; font-weight: 700; }}
        .risk-low {{ color: #2e8b57; font-weight: 700; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
