"""Hidden instructor numerical panel."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from hegemony_calculator.core.models import GameState
from hegemony_calculator.core.welfare import minimum_income_for_domain, to_game_params, welfare_gap
from hegemony_calculator.engine.income_solver import build_welfare_inputs, numeric_results_dataframe


def render_engine_panel(state: GameState) -> None:
    """Render the collapsible instructor panel."""

    snapshot = state.last_numeric_snapshot
    with st.sidebar.expander("Motor de Analisis Numerico", expanded=False):
        if snapshot is None:
            st.info("El motor se activa al iniciar o resolver una fase.")
            return

        st.metric("Ingreso minimo I*", f"{snapshot.required_income:.2f}V")
        st.caption(f"Meta continua S*={snapshot.target_welfare:.3f}")
        st.dataframe(numeric_results_dataframe(snapshot), hide_index=True, width="stretch")

        params = to_game_params(build_welfare_inputs(state, snapshot.actual_income))
        lower = minimum_income_for_domain(params)
        upper = max(snapshot.required_income * 1.5, lower + 100.0)
        step = (upper - lower) / 80
        xs = [lower + (index * step) for index in range(81)]
        ys = [welfare_gap(x, params) for x in xs]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name="f(I)"))
        fig.add_hline(y=0, line_dash="dash", line_color="#a53d3d")
        fig.add_vline(x=snapshot.required_income, line_dash="dot", line_color="#2d6fba")
        fig.update_layout(height=260, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, width="stretch")

        rows: list[dict[str, float | int | str]] = []
        for result in snapshot.results:
            for step in result.history:
                rows.append(
                    {
                        "Metodo": result.method_name,
                        "Iteracion": step.iteration,
                        "Error": max(step.relative_error or 1e-12, 1e-12),
                    }
                )
        if rows:
            error_df = pd.DataFrame(rows)
            st.line_chart(error_df, x="Iteracion", y="Error", color="Metodo")
