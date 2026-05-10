"""Production phase screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import GameState
from hegemony_calculator.engine.game_engine import advance_phase


def render_production(state: GameState) -> None:
    """Render production narration."""

    st.subheader("Fase de Produccion")
    st.write("Las empresas producen, se pagan salarios, se cubren necesidades y entran impuestos.")
    for message in state.narrative_log[-6:]:
        st.markdown(f'<div class="narrative-line">{message}</div>', unsafe_allow_html=True)
    if st.button("Resolver siguiente fase", width="stretch"):
        advance_phase(state)
        st.session_state["game_state"] = state
        st.rerun()
