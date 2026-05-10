"""Hidden income solver that translates numerical roots into game narration."""

from __future__ import annotations

import pandas as pd

from hegemony_calculator.services.calculator import WelfareCalculatorService
from hegemony_calculator.core.models import ClassRole, GameState, NumericEngineSnapshot
from hegemony_calculator.core.welfare import WelfareInputs, to_game_params
from hegemony_calculator.engine.tax_calculator import effective_tax_rate


HEALTH_PRICE_BY_POLICY: dict[str, float] = {"A": 0.75, "B": 5.0, "C": 10.0}
EDUCATION_PRICE_BY_POLICY: dict[str, float] = {"A": 0.75, "B": 5.0, "C": 10.0}
FOOD_PRICE_BY_TRADE: dict[str, float] = {"A": 6.0, "B": 4.0, "C": 3.0}
LUXURY_PRICE_BY_TRADE: dict[str, float] = {"A": 14.0, "B": 10.0, "C": 8.0}


def prosperity_to_welfare_target(prosperity_goal: int) -> float:
    """Map a board prosperity target to the continuous welfare scale."""

    return 1.65 + (prosperity_goal * 0.33)


def build_welfare_inputs(state: GameState, actual_income: float) -> WelfareInputs:
    """Build hidden welfare parameters from the current board state."""

    player = state.players[ClassRole.WORKING]
    tax_rate = effective_tax_rate(actual_income, player.population, state.policies)
    return WelfareInputs(
        population=player.population,
        tax_rate=tax_rate,
        food_available=player.resources.food,
        food_price=FOOD_PRICE_BY_TRADE[state.policies.foreign_trade],
        health_available=player.resources.health,
        education_available=player.resources.education,
        luxury_available=player.resources.luxury,
        health_price=HEALTH_PRICE_BY_POLICY[state.policies.public_health],
        education_price=EDUCATION_PRICE_BY_POLICY[state.policies.public_education],
        luxury_price=LUXURY_PRICE_BY_TRADE[state.policies.foreign_trade],
        target_welfare=prosperity_to_welfare_target(player.prosperity_goal),
    )


def solve_income_need(state: GameState, actual_income: float | None = None) -> NumericEngineSnapshot:
    """Run all numerical methods and return a narrative snapshot."""

    income = float(state.last_income if actual_income is None else actual_income)
    inputs = build_welfare_inputs(state, income)
    params = to_game_params(inputs)
    summary = WelfareCalculatorService(tolerance=1e-7, max_iterations=200).solve_all(params)
    required_income = summary.consensus_root or 0.0
    player = state.players[ClassRole.WORKING]
    gap = max(0.0, required_income - income)

    if income >= required_income:
        narrative = (
            f"Con {income:.0f}V netos puedes sostener la meta de Prosperidad "
            f"{player.prosperity_goal}. Conviene asegurar bienes antes de la votacion."
        )
    else:
        narrative = (
            f"Con {income:.0f}V netos aun faltan {gap:.0f}V para llegar a "
            f"Prosperidad {player.prosperity_goal}. Huelga, mas empleo o salud publica ayudan."
        )

    snapshot = NumericEngineSnapshot(
        required_income=required_income,
        actual_income=income,
        target_welfare=inputs.target_welfare,
        results=summary.results,
        narrative=narrative,
    )
    state.last_numeric_snapshot = snapshot
    state.narrative_log.append(narrative)
    return snapshot


def numeric_results_dataframe(snapshot: NumericEngineSnapshot) -> pd.DataFrame:
    """Return the hidden instructor comparison table."""

    return pd.DataFrame(
        [
            {
                "Metodo": result.method_name,
                "I*": result.root,
                "Iteraciones": result.iterations,
                "Error": result.final_error,
                "Tiempo ms": result.execution_time_ms,
                "Convergio": result.converged,
            }
            for result in snapshot.results
        ]
    )

