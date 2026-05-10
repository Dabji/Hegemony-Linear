"""Worker grid component."""

from __future__ import annotations

import streamlit as st


def render_worker_grid(population: int, employed: int, qualified: int) -> None:
    """Render workers as compact visual tokens."""

    tokens: list[str] = []
    for index in range(population):
        if index < qualified:
            css_class = "worker qualified"
        elif index < employed:
            css_class = "worker employed"
        else:
            css_class = "worker idle"
        tokens.append(f'<span class="{css_class}"></span>')
    st.markdown(f'<div class="worker-grid">{"".join(tokens)}</div>', unsafe_allow_html=True)

