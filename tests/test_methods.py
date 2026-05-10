"""Tests for the hidden numerical game engine."""

from __future__ import annotations

import math

from hegemony_calculator.engine.game_engine import new_game
from hegemony_calculator.engine.income_solver import solve_income_need


def test_hidden_income_solver_runs_all_methods() -> None:
    state = new_game()
    snapshot = solve_income_need(state, actual_income=120)
    assert len(snapshot.results) == 5
    assert all(result.converged for result in snapshot.results)

    roots = [result.root for result in snapshot.results]
    baseline = roots[0]
    for root in roots[1:]:
        assert math.isclose(root, baseline, rel_tol=1e-3, abs_tol=0.5)


def test_income_solver_returns_game_narrative_not_formula() -> None:
    state = new_game()
    snapshot = solve_income_need(state, actual_income=60)
    assert "Prosperidad" in snapshot.narrative
    assert "f(I)" not in snapshot.narrative

