"""Prosperity progress component."""

from __future__ import annotations

import streamlit as st


def render_prosperity_bar(current: int, goal: int) -> None:
    """Render prosperity progress."""

    st.markdown(f"**Prosperidad {current}/10**")
    st.progress(current / 10)
    st.caption(f"Meta de ronda: Prosperidad {goal}")

