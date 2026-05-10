"""Unit tests for the Newton-Raphson method."""

from __future__ import annotations

from hegemony_calculator.core.methods.newton_raphson import NewtonRaphsonMethod
from hegemony_calculator.core.models import GameParams
from hegemony_calculator.core.welfare import welfare_gap


def build_params() -> GameParams:
    """Return a root-finding scenario for Newton-Raphson."""

    return GameParams(
        population=120,
        tax_rate=0.22,
        food_available=85.0,
        food_price=1.8,
        health_initial=3.0,
        education_initial=4.0,
        leisure_initial=2.0,
        health_price=9.0,
        education_price=11.0,
        leisure_price=6.5,
        health_budget_ratio=0.45,
        education_budget_ratio=0.25,
        leisure_budget_ratio=0.30,
        health_weight=0.5,
        education_weight=0.2,
        leisure_weight=0.3,
        target_welfare=3.25,
        bracket_low=0.0,
        bracket_high=4_000.0,
        initial_guess=700.0,
        secondary_guess=900.0,
    )


def test_newton_converges_to_root() -> None:
    params = build_params()
    result = NewtonRaphsonMethod(params, tolerance=1e-7, max_iterations=100).solve()
    assert result.converged
    assert abs(welfare_gap(result.root, params)) < 1e-6

