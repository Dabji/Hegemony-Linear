"""Validation tests for input parameters."""

from __future__ import annotations

import pytest

from hegemony_calculator.services.validator import InputValidationError, validate_game_params


def test_validate_game_params_accepts_valid_payload() -> None:
    params = validate_game_params(
        {
            "population": 100,
            "tax_rate": 0.2,
            "food_available": 80,
            "food_price": 1.5,
            "health_initial": 5,
            "education_initial": 4,
            "leisure_initial": 3,
            "health_price": 10,
            "education_price": 12,
            "leisure_price": 8,
            "health_budget_ratio": 0.4,
            "education_budget_ratio": 0.35,
            "leisure_budget_ratio": 0.25,
            "health_weight": 0.4,
            "education_weight": 0.35,
            "leisure_weight": 0.25,
            "target_welfare": 2.5,
        }
    )
    assert params.population == 100


def test_validate_game_params_rejects_invalid_ratios() -> None:
    with pytest.raises(InputValidationError):
        validate_game_params(
            {
                "population": 100,
                "tax_rate": 0.2,
                "food_available": 80,
                "food_price": 1.5,
                "health_initial": 5,
                "education_initial": 4,
                "leisure_initial": 3,
                "health_price": 10,
                "education_price": 12,
                "leisure_price": 8,
                "health_budget_ratio": 0.5,
                "education_budget_ratio": 0.35,
                "leisure_budget_ratio": 0.25,
                "health_weight": 0.4,
                "education_weight": 0.35,
                "leisure_weight": 0.25,
                "target_welfare": 2.5,
            }
        )
