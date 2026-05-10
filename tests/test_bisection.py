"""Unit tests for the bisection method."""

from __future__ import annotations

from hegemony_calculator.core.methods.bisection import BisectionMethod
from hegemony_calculator.core.models import GameParams
from hegemony_calculator.core.welfare import welfare_gap


def build_params() -> GameParams:
    """Return a bracketed test case."""

    return GameParams(
        population=100,
        tax_rate=0.15,
        food_available=90.0,
        food_price=1.5,
        health_initial=4.0,
        education_initial=3.5,
        leisure_initial=5.0,
        health_price=8.0,
        education_price=9.5,
        leisure_price=7.0,
        health_budget_ratio=0.4,
        education_budget_ratio=0.3,
        leisure_budget_ratio=0.3,
        health_weight=0.34,
        education_weight=0.33,
        leisure_weight=0.33,
        target_welfare=3.1,
        bracket_low=0.0,
        bracket_high=3_000.0,
        initial_guess=800.0,
        secondary_guess=900.0,
    )


def test_bisection_converges_to_root() -> None:
    params = build_params()
    result = BisectionMethod(params, tolerance=1e-7, max_iterations=200).solve()
    assert result.converged
    assert abs(welfare_gap(result.root, params)) < 1e-6

