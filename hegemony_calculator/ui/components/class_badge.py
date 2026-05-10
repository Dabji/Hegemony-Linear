"""Class role badge component."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import ClassRole


ROLE_COLORS: dict[ClassRole, str] = {
    ClassRole.WORKING: "#c83f3f",
    ClassRole.MIDDLE: "#d8aa2b",
    ClassRole.CAPITALIST: "#2d6fba",
    ClassRole.STATE: "#7d858c",
}


def render_class_badge(role: ClassRole, compact: bool = False) -> None:
    """Render a class badge."""

    color = ROLE_COLORS[role]
    padding = "4px 8px" if compact else "8px 12px"
    st.markdown(
        f"""
        <div style="display:inline-block;background:{color};color:white;padding:{padding};
                    border-radius:6px;font-weight:700;font-size:0.9rem;">
            {role.value}
        </div>
        """,
        unsafe_allow_html=True,
    )

