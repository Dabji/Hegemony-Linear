"""Unit tests for the welfare model."""

from __future__ import annotations

import math

from hegemony_calculator.core.models import GameParams
from hegemony_calculator.core.welfare import (
    free_budget,
    mandatory_food_cost,
    welfare,
    welfare_gap,
    welfare_gap_derivative,
)


def build_params() -> GameParams:
    """Create a representative parameter set for tests."""

    return GameParams(
        population=100,
        tax_rate=0.2,
        food_available=70.0,
        food_price=2.0,
        health_initial=5.0,
        education_initial=3.0,
        leisure_initial=4.0,
        health_price=10.0,
        education_price=12.0,
        leisure_price=8.0,
        health_budget_ratio=0.4,
        education_budget_ratio=0.35,
        leisure_budget_ratio=0.25,
        health_weight=0.4,
        education_weight=0.35,
        leisure_weight=0.25,
        target_welfare=2.95,
    )


def test_mandatory_food_cost_uses_only_missing_food() -> None:
    params = build_params()
    assert math.isclose(mandatory_food_cost(params), 60.0)


def test_free_budget_applies_taxes_and_mandatory_food() -> None:
    params = build_params()
    assert math.isclose(free_budget(200.0, params), 100.0)


def test_welfare_returns_expected_value() -> None:
    params = build_params()
    result = welfare(200.0, params)
    assert math.isclose(result, 2.121647354554578, rel_tol=1e-9)


def test_welfare_gap_matches_target_difference() -> None:
    params = build_params()
    result = welfare_gap(200.0, params)
    assert math.isclose(result, welfare(200.0, params) - 2.95, rel_tol=1e-9)


def test_welfare_gap_derivative_is_positive_for_valid_income() -> None:
    params = build_params()
    derivative = welfare_gap_derivative(200.0, params)
    assert derivative > 0.0
