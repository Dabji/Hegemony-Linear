"""Streamlit application for the playable Hegemony game."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

for candidate in Path(__file__).resolve().parents:
    if (candidate / "hegemony_calculator").is_dir():
        if str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
        break

from hegemony_calculator.core.models import GamePhase, GameState
from hegemony_calculator.engine.game_engine import new_game
from hegemony_calculator.ui.screens.action_phase import render_action_phase
from hegemony_calculator.ui.screens.board import render_board
from hegemony_calculator.ui.screens.elections import render_elections
from hegemony_calculator.ui.screens.engine_panel import render_engine_panel
from hegemony_calculator.ui.screens.intro import render_intro
from hegemony_calculator.ui.screens.production import render_production
from hegemony_calculator.ui.screens.scoring import render_scoring


def _inject_styles() -> None:
    """Inject game-specific CSS."""

    st.markdown(
        """
        <style>
        .stApp { background: #f4f1ea; color: #211b18; }
        [data-testid="stSidebar"] { background: #20252b; color: #f7f3e8; }
        .intro-band {
            min-height: 68vh;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #161a21 0%, #4b1f24 45%, #153a4a 100%);
            color: #f8efe2;
        }
        .worker-grid { display:grid; grid-template-columns:repeat(10, 18px); gap:6px; margin:8px 0 12px; }
        .worker { width:18px; height:18px; border-radius:4px; display:inline-block; border:1px solid rgba(0,0,0,0.25); }
        .worker.employed { background:#c83f3f; }
        .worker.qualified { background:#f0c84b; }
        .worker.idle { background:#d1d5db; }
        .round-track { display:flex; gap:10px; margin:4px 0 16px; }
        .round-dot {
            width:34px; height:34px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center;
            border:2px solid #80776a; color:#4c4439; font-weight:700;
        }
        .round-dot.active { background:#1f6f8b; color:white; border-color:#1f6f8b; }
        .narrative-line {
            padding:10px 12px; margin:6px 0; border-left:4px solid #1f6f8b;
            background:#fffaf0; border-radius:6px; box-shadow:0 1px 0 rgba(0,0,0,0.05);
        }
        div[data-testid="stMetric"] {
            background:#fffaf0; padding:10px; border-radius:6px; border:1px solid #dfd5c2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _state() -> GameState | None:
    """Return the current game state from session."""

    return st.session_state.get("game_state")


def main() -> None:
    """Render the game."""

    st.set_page_config(page_title="Hegemony Game", page_icon=":bar_chart:", layout="wide")
    _inject_styles()

    if not st.session_state.get("game_started"):
        render_intro()
        return

    state = _state()
    if state is None:
        st.session_state["game_state"] = new_game()
        state = st.session_state["game_state"]

    with st.sidebar:
        st.title("Hegemony")
        st.caption(f"Ronda {state.round_number}/5 | Fase {state.phase.value}")
        if st.button("Nueva partida", width="stretch"):
            for key in ("game_state", "game_started"):
                st.session_state.pop(key, None)
            st.rerun()
        render_engine_panel(state)

    board_tab, action_tab, production_tab, election_tab, scoring_tab = st.tabs(
        ["Tablero", "Accion", "Produccion", "Elecciones", "Puntuacion"]
    )
    with board_tab:
        render_board(state)
    with action_tab:
        render_action_phase(state)
    with production_tab:
        if state.phase != GamePhase.PRODUCTION:
            st.info("La produccion se resuelve al avanzar a la fase correspondiente.")
        render_production(state)
    with election_tab:
        render_elections(state)
    with scoring_tab:
        render_scoring(state)


if __name__ == "__main__":
    main()
