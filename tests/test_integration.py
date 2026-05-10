"""Integration tests for the full calculator workflow."""

from __future__ import annotations

import math

from hegemony_calculator.core.models import GameParams
from hegemony_calculator.services.calculator import WelfareCalculatorService


def build_params() -> GameParams:
    """Return a consistent scenario for all methods."""

    return GameParams(
        population=140,
        tax_rate=0.18,
        food_available=100.0,
        food_price=2.0,
        health_initial=5.0,
        education_initial=4.0,
        leisure_initial=3.0,
        health_price=10.0,
        education_price=12.0,
        leisure_price=7.0,
        health_budget_ratio=0.38,
        education_budget_ratio=0.32,
        leisure_budget_ratio=0.30,
        health_weight=0.45,
        education_weight=0.30,
        leisure_weight=0.25,
        target_welfare=3.45,
        bracket_low=0.0,
        bracket_high=5_000.0,
        initial_guess=900.0,
        secondary_guess=1_100.0,
    )


def test_all_methods_converge_to_similar_root() -> None:
    params = build_params()
    service = WelfareCalculatorService(tolerance=1e-7, max_iterations=200)
    summary = service.solve_all(params)

    converged_results = [result for result in summary.results if result.converged]
    assert len(converged_results) == 5

    baseline = converged_results[0].root
    for result in converged_results[1:]:
        assert math.isclose(result.root, baseline, rel_tol=1e-4, abs_tol=1e-3)
