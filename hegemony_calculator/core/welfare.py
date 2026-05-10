"""Pure mathematical functions for the welfare model."""

from __future__ import annotations

import math
from dataclasses import dataclass

from hegemony_calculator.core.models import GameParams


def mandatory_food_cost(params: GameParams) -> float:
    """Return the mandatory food expenditure for the worker class."""

    return params.food_cost


def free_budget(income: float, params: GameParams) -> float:
    """Return free budget after taxes and mandatory food cost."""

    return income * (1.0 - params.tax_rate) - mandatory_food_cost(params)


def welfare_components(income: float, params: GameParams) -> tuple[float, float, float]:
    """Return the effective health, education, and leisure levels."""

    budget = free_budget(income, params)
    health_total = params.health_initial + (params.health_budget_ratio * budget / params.health_price)
    education_total = (
        params.education_initial + (params.education_budget_ratio * budget / params.education_price)
    )
    leisure_total = params.leisure_initial + (params.leisure_budget_ratio * budget / params.leisure_price)
    return health_total, education_total, leisure_total


def welfare(income: float, params: GameParams) -> float:
    """Evaluate the nonlinear worker welfare function W(I)."""

    health_total, education_total, leisure_total = welfare_components(income, params)
    if min(health_total, education_total, leisure_total) <= -1.0:
        raise ValueError("Income produces an invalid welfare state for the logarithm domain.")

    return (
        params.health_weight * math.log1p(health_total)
        + params.education_weight * math.log1p(education_total)
        + params.leisure_weight * math.log1p(leisure_total)
    )


def welfare_gap(income: float, params: GameParams) -> float:
    """Evaluate f(I) = W(I) - S*."""

    return welfare(income, params) - params.target_welfare


def welfare_gap_derivative(income: float, params: GameParams) -> float:
    """Evaluate the analytical derivative f'(I) for Newton-Raphson."""

    health_total, education_total, leisure_total = welfare_components(income, params)
    return (1.0 - params.tax_rate) * (
        (params.health_weight * params.health_budget_ratio / params.health_price) / (1.0 + health_total)
        + (params.education_weight * params.education_budget_ratio / params.education_price)
        / (1.0 + education_total)
        + (params.leisure_weight * params.leisure_budget_ratio / params.leisure_price) / (1.0 + leisure_total)
    )


def minimum_income_for_domain(params: GameParams, margin: float = 1e-6) -> float:
    """Return the minimum income that keeps all logarithm arguments positive."""

    required_budget = float("-inf")
    constraints = (
        (params.health_initial, params.health_budget_ratio, params.health_price),
        (params.education_initial, params.education_budget_ratio, params.education_price),
        (params.leisure_initial, params.leisure_budget_ratio, params.leisure_price),
    )

    for initial_value, ratio, price in constraints:
        if ratio == 0:
            continue
        required_budget = max(required_budget, ((-1.0 - initial_value + margin) * price) / ratio)

    if required_budget == float("-inf"):
        return 0.0

    gross_income = (required_budget + mandatory_food_cost(params)) / max(1.0 - params.tax_rate, 1e-12)
    return max(0.0, gross_income)


@dataclass(slots=True)
class WelfareInputs:
    """Board-derived inputs for the hidden numerical engine."""

    population: int
    tax_rate: float
    food_available: float
    food_price: float
    health_available: float
    education_available: float
    luxury_available: float
    health_price: float
    education_price: float
    luxury_price: float
    target_welfare: float


def to_game_params(inputs: WelfareInputs) -> GameParams:
    """Convert board-derived welfare inputs into numerical parameters."""

    return GameParams(
        population=inputs.population,
        tax_rate=inputs.tax_rate,
        food_available=inputs.food_available,
        food_price=max(inputs.food_price, 0.01),
        health_initial=inputs.health_available,
        education_initial=inputs.education_available,
        leisure_initial=inputs.luxury_available,
        health_price=max(inputs.health_price, 0.01),
        education_price=max(inputs.education_price, 0.01),
        leisure_price=max(inputs.luxury_price, 0.01),
        health_budget_ratio=0.40,
        education_budget_ratio=0.35,
        leisure_budget_ratio=0.25,
        health_weight=0.40,
        education_weight=0.35,
        leisure_weight=0.25,
        target_welfare=inputs.target_welfare,
        bracket_low=0.0,
        bracket_high=5_000.0,
        initial_guess=600.0,
        secondary_guess=900.0,
    )
