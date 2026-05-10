"""Validation service for application inputs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from hegemony_calculator.config import (
    DEFAULT_BRACKET,
    DEFAULT_FIXED_POINT_K,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_SECANT_GUESS,
    DEFAULT_TOLERANCE,
)
from hegemony_calculator.core.models import GameParams


class InputValidationError(Exception):
    """Raised when the user input is invalid."""


class GameParamsInput(BaseModel):
    """Pydantic schema for validating form input."""

    model_config = ConfigDict(str_strip_whitespace=True)

    population: int = Field(gt=0)
    tax_rate: float = Field(ge=0.0, le=1.0)
    food_available: float = Field(ge=0.0)
    food_price: float = Field(gt=0.0)
    health_initial: float = Field(ge=0.0)
    education_initial: float = Field(ge=0.0)
    leisure_initial: float = Field(ge=0.0)
    health_price: float = Field(gt=0.0)
    education_price: float = Field(gt=0.0)
    leisure_price: float = Field(gt=0.0)
    health_budget_ratio: float = Field(ge=0.0, le=1.0)
    education_budget_ratio: float = Field(ge=0.0, le=1.0)
    leisure_budget_ratio: float = Field(ge=0.0, le=1.0)
    health_weight: float = Field(ge=0.0, le=1.0)
    education_weight: float = Field(ge=0.0, le=1.0)
    leisure_weight: float = Field(ge=0.0, le=1.0)
    target_welfare: float = Field(gt=0.0)
    fixed_point_k: float = Field(default=DEFAULT_FIXED_POINT_K, gt=0.0)
    bracket_low: float = Field(default=DEFAULT_BRACKET[0], ge=0.0)
    bracket_high: float = Field(default=DEFAULT_BRACKET[1], gt=0.0)
    initial_guess: float = Field(default=DEFAULT_SECANT_GUESS[0], ge=0.0)
    secondary_guess: float = Field(default=DEFAULT_SECANT_GUESS[1], ge=0.0)
    tolerance: float = Field(default=DEFAULT_TOLERANCE, gt=0.0)
    max_iterations: int = Field(default=DEFAULT_MAX_ITERATIONS, gt=0)

    @model_validator(mode="after")
    def validate_sums(self) -> "GameParamsInput":
        """Validate ratio and weight sums plus interval consistency."""

        budget_sum = self.health_budget_ratio + self.education_budget_ratio + self.leisure_budget_ratio
        weight_sum = self.health_weight + self.education_weight + self.leisure_weight

        if abs(budget_sum - 1.0) > 1e-9:
            raise ValueError("Budget ratios must sum to 1.")
        if abs(weight_sum - 1.0) > 1e-9:
            raise ValueError("Utility weights must sum to 1.")
        if self.bracket_high <= self.bracket_low:
            raise ValueError("The upper bracket must be greater than the lower bracket.")
        if self.secondary_guess == self.initial_guess:
            raise ValueError("Initial guesses for the secant method must be different.")
        return self


def validate_game_params(payload: dict[str, Any]) -> GameParams:
    """Validate raw input and return a typed domain model."""

    try:
        validated = GameParamsInput.model_validate(payload)
    except ValidationError as exc:
        raise InputValidationError(str(exc)) from exc
    except ValueError as exc:
        raise InputValidationError(str(exc)) from exc

    data = validated.model_dump(exclude={"tolerance", "max_iterations"})
    return GameParams(**data)

