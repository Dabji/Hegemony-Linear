"""Resource token display."""

from __future__ import annotations

import streamlit as st

from hegemony_calculator.core.models import Resources


def render_resource_tokens(resources: Resources) -> None:
    """Render resources as compact metrics."""

    labels = [
        ("Vardis", resources.vardis),
        ("Comida", resources.food),
        ("Salud", resources.health),
        ("Educacion", resources.education),
        ("Ocio", resources.luxury),
        ("Influencia", resources.influence),
    ]
    columns = st.columns(3)
    for index, (label, value) in enumerate(labels):
        with columns[index % 3]:
            st.metric(label, value)

