"""Tests for the playable game engine."""

from __future__ import annotations

from hegemony_calculator.core.models import GamePhase
from hegemony_calculator.engine.game_engine import advance_phase, assign_worker, buy_and_use_resource, new_game, strike


def test_assign_worker_updates_board_and_narrative() -> None:
    state = new_game()
    before = sum(company.assigned_workers for company in state.companies)
    message = assign_worker(state)
    after = sum(company.assigned_workers for company in state.companies)
    assert after == before + 1
    assert "obrero" in message


def test_buy_health_can_raise_prosperity_when_affordable() -> None:
    state = new_game()
    player = state.active_player
    player.resources.vardis = 500
    before = player.prosperity
    buy_and_use_resource(state, "health")
    assert player.prosperity == before + 1
    assert player.population == 11


def test_phase_advancement_reaches_production() -> None:
    state = new_game()
    state.phase = GamePhase.ACTION
    advance_phase(state)
    assert state.phase == GamePhase.PRODUCTION
    assert state.last_income >= 0


def test_strike_adds_influence() -> None:
    state = new_game()
    before = state.active_player.resources.influence
    strike(state)
    assert state.active_player.resources.influence == before + 2

