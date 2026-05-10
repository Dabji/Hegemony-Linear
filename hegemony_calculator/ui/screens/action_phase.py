"""Action phase screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import GamePhase, GameState
from hegemony_calculator.engine.game_engine import (
    advance_phase,
    assign_worker,
    buy_and_use_resource,
    propose_law,
    set_prosperity_goal,
    strike,
)


def render_action_phase(state: GameState) -> None:
    """Render contextual player actions."""

    st.subheader("Turno de accion")
    player = state.active_player
    goal_options = list(range(player.prosperity + 1, 11))
    if goal_options:
        selected_goal = st.radio("Meta de Prosperidad de la ronda", goal_options, horizontal=True, index=0)
        if selected_goal != player.prosperity_goal:
            set_prosperity_goal(state, selected_goal)

    columns = st.columns(3)
    actions = [
        ("Asignar Obreros", assign_worker, state.phase == GamePhase.ACTION),
        ("Comprar Salud", lambda current: buy_and_use_resource(current, "health"), True),
        ("Comprar Educacion", lambda current: buy_and_use_resource(current, "education"), True),
        ("Comprar Ocio", lambda current: buy_and_use_resource(current, "luxury"), True),
        ("Comprar Comida", lambda current: buy_and_use_resource(current, "food"), True),
        ("Hacer Huelga", strike, state.phase == GamePhase.ACTION),
        ("Proponer Ley", propose_law, True),
    ]

    for index, (label, handler, enabled) in enumerate(actions):
        with columns[index % 3]:
            if st.button(label, disabled=not enabled, width="stretch"):
                handler(state)
                st.session_state["game_state"] = state
                st.rerun()

    if st.button("Avanzar fase", type="primary", width="stretch"):
        advance_phase(state)
        st.session_state["game_state"] = state
        st.rerun()

    if state.last_numeric_snapshot is not None:
        st.info(state.last_numeric_snapshot.narrative)
