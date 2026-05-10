"""Policy table component."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from hegemony_calculator.core.models import Policies


POLICY_LABELS: dict[str, str] = {
    "fiscal": "Politica Fiscal",
    "labor_market": "Mercado Laboral",
    "taxation": "Tributacion",
    "public_health": "Bienestar Salud",
    "public_education": "Bienestar Educacion",
    "foreign_trade": "Comercio Exterior",
    "immigration": "Inmigracion",
}


def render_policy_table(policies: Policies) -> None:
    """Render current policies."""

    rows = [{"Politica": label, "Actual": getattr(policies, key)} for key, label in POLICY_LABELS.items()]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
