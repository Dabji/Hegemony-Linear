"""Main board screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import ClassRole, GameState
from hegemony_calculator.ui.components.company_card import render_company_card
from hegemony_calculator.ui.components.narrative_box import render_narrative_box
from hegemony_calculator.ui.components.policy_table import render_policy_table
from hegemony_calculator.ui.screens.player_board import render_player_board


def render_round_tracker(state: GameState) -> None:
    """Render five-round tracker."""

    circles = []
    for round_number in range(1, 6):
        css_class = "round-dot active" if round_number == state.round_number else "round-dot"
        circles.append(f'<span class="{css_class}">{round_number}</span>')
    st.markdown(f'<div class="round-track">{"".join(circles)}</div>', unsafe_allow_html=True)


def render_board(state: GameState) -> None:
    """Render the board and player panel."""

    st.subheader(f"Ronda {state.round_number} | Fase de {state.phase.value}")
    render_round_tracker(state)

    top_left, top_right = st.columns([1.2, 1])
    with top_left:
        st.markdown("**Politicas vigentes**")
        render_policy_table(state.policies)
    with top_right:
        render_player_board(state)

    st.markdown("**Empresas del tablero**")
    private, public = st.columns(2)
    with private:
        st.markdown("Sector Privado")
        for company in [item for item in state.companies if not item.is_public]:
            render_company_card(company)
    with public:
        st.markdown("Sector Publico")
        for company in [item for item in state.companies if item.is_public]:
            render_company_card(company)

    render_narrative_box(state.narrative_log)
    other = state.players[ClassRole.CAPITALIST]
    st.caption(f"Capital acumulado capitalista: {other.capital}V | Legitimidad estatal: {state.players[ClassRole.STATE].legitimacy}")

