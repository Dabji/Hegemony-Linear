"""Scoring screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import ClassRole, GameState
from hegemony_calculator.engine.game_engine import advance_phase


def render_scoring(state: GameState) -> None:
    """Render round scoring."""

    st.subheader("Puntuacion de ronda")
    players = state.players
    columns = st.columns(4)
    for column, role in zip(columns, ClassRole):
        with column:
            player = players[role]
            value = player.victory_points if role != ClassRole.CAPITALIST else player.capital
            st.metric(role.value, value)

    for message in state.narrative_log[-5:]:
        st.markdown(f'<div class="narrative-line">{message}</div>', unsafe_allow_html=True)

    label = "Finalizar partida" if state.round_number >= 5 else "Siguiente ronda"
    if st.button(label, type="primary", width="stretch"):
        advance_phase(state)
        st.session_state["game_state"] = state
        st.rerun()
