"""Player board screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import GameState
from hegemony_calculator.ui.components.prosperity_bar import render_prosperity_bar
from hegemony_calculator.ui.components.resource_tokens import render_resource_tokens
from hegemony_calculator.ui.components.worker_grid import render_worker_grid


def render_player_board(state: GameState) -> None:
    """Render the selected player's board."""

    player = state.active_player
    st.subheader("Tablero del jugador")
    render_prosperity_bar(player.prosperity, player.prosperity_goal)
    render_resource_tokens(player.resources)
    st.markdown("**Poblacion trabajadora**")
    render_worker_grid(player.population, player.employed_workers, player.qualified_workers)
    st.caption(f"PV: {player.victory_points} | Sindicatos: {player.unions}")

