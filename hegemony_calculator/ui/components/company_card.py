"""Company card component."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import Company
from hegemony_calculator.ui.components.class_badge import render_class_badge


def render_company_card(company: Company) -> None:
    """Render a board company card."""

    with st.container(border=True):
        st.markdown(f"**{company.name}**")
        st.caption(company.industry)
        render_class_badge(company.owner, compact=True)
        slots = " ".join("[X]" if index < company.assigned_workers else "[ ]" for index in range(company.worker_slots))
        st.markdown(f"`{slots}`")
        st.caption(f"Produce {company.output_amount} {company.output_resource} por obrero")
        st.caption(f"Salario L{company.wage_level}{' | Publica' if company.is_public else ''}")
