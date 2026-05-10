"""Intro and class selection screen."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import ClassRole
from hegemony_calculator.engine.game_engine import new_game
from hegemony_calculator.ui.components.class_badge import render_class_badge


ROLE_COPY: dict[ClassRole, str] = {
    ClassRole.WORKING: "Convierte salarios, bienes y presion politica en Prosperidad.",
    ClassRole.MIDDLE: "Equilibra pequenos negocios, consumo y estabilidad social.",
    ClassRole.CAPITALIST: "Controla empresas, salarios y capital de inversion.",
    ClassRole.STATE: "Sostiene legitimidad mientras todos empujan la ley hacia su lado.",
}


def render_intro() -> None:
    """Render the playable intro."""

    st.markdown('<section class="intro-band">', unsafe_allow_html=True)
    st.title("HEGEMONY")
    st.markdown("### Lead Your Class to Victory")
    st.write("Elige una clase y empieza una partida de 5 rondas. El motor numerico trabaja oculto.")
    players_count = st.radio("Jugadores", [1, 2, 3, 4], horizontal=True, index=0)
    columns = st.columns(4)
    for column, role in zip(columns, ClassRole):
        with column:
            with st.container(border=True):
                render_class_badge(role)
                st.write(ROLE_COPY[role])
                if st.button("Elegir", key=f"choose_{role.value}", width="stretch"):
                    st.session_state["game_state"] = new_game(role, players_count)
                    st.session_state["game_started"] = True
                    st.rerun()
    st.markdown("</section>", unsafe_allow_html=True)
