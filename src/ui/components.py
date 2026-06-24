from __future__ import annotations

import streamlit as st


def page_title(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)


def insight(text: str) -> None:
    st.markdown(f"<div class='insight-box'>{text}</div>", unsafe_allow_html=True)


def section(label: str) -> None:
    st.subheader(label)


def dataframe(df, height: int = 320) -> None:
    st.dataframe(df, use_container_width=True, height=height)

