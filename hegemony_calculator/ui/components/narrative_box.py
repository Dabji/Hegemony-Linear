"""Narrative log component."""

from __future__ import annotations

import streamlit as st


def render_narrative_box(messages: list[str], limit: int = 5) -> None:
    """Render recent game narrative."""

    st.markdown("**Cronica de la ronda**")
    for message in messages[-limit:][::-1]:
        st.markdown(f'<div class="narrative-line">{message}</div>', unsafe_allow_html=True)

