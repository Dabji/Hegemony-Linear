"""Election screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import GameState
from hegemony_calculator.engine.game_engine import resolve_current_election


def render_elections(state: GameState) -> None:
    """Render election controls."""

    st.subheader("Elecciones")
    proposal = state.election_proposal
    if proposal is None:
        st.info("No hay ley pendiente. Propone una ley desde la fase de accion.")
        return

    st.markdown(f"**Ley propuesta:** {proposal.title}")
    max_influence = state.active_player.resources.influence
    influence = st.slider("Influencia a gastar", min_value=0, max_value=max_influence, value=min(2, max_influence))
    if st.button("Sacar 5 cubos y votar", type="primary", width="stretch"):
        resolve_current_election(state, influence)
        st.session_state["game_state"] = state
        st.rerun()

    for message in state.narrative_log[-4:]:
        st.markdown(f'<div class="narrative-line">{message}</div>', unsafe_allow_html=True)
