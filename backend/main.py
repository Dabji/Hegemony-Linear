"""FastAPI entrypoint for the Hegemony numerical engine."""

from __future__ import annotations

import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hegemony_calculator.core.methods.base import NumericalMethodError
from hegemony_calculator.core.methods.newton_raphson import NewtonRaphsonMethod
from hegemony_calculator.core.models import GameParams
from hegemony_calculator.core.welfare import (
    free_budget,
    mandatory_food_cost,
    minimum_income_for_domain,
    welfare,
)
from hegemony_calculator.services.calculator import WelfareCalculatorService


class IncomeRequest(BaseModel):
    """Board state sent by the React app.

    The aliases accept mathematical names from the project statement
    (`P`, `tau`, `H0`, `S*`) and readable API names (`population`,
    `tax_rate`, `health_initial`, `target_welfare`).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    population: int = Field(10, validation_alias=AliasChoices("P", "population"), ge=1, le=200)
    tax_rate: float = Field(0.22, validation_alias=AliasChoices("tau", "tax_rate"), ge=0.0, lt=0.95)
    food_available: float = Field(4.0, validation_alias=AliasChoices("F0", "food_available"), ge=0.0)
    food_price: float = Field(4.0, validation_alias=AliasChoices("p_f", "food_price"), gt=0.0)
    health_initial: float = Field(0.0, validation_alias=AliasChoices("H0", "health_initial"), ge=0.0)
    education_initial: float = Field(0.0, validation_alias=AliasChoices("E0", "education_initial"), ge=0.0)
    leisure_initial: float = Field(0.0, validation_alias=AliasChoices("L0", "leisure_initial", "luxury_initial"), ge=0.0)
    health_price: float = Field(5.0, validation_alias=AliasChoices("p_h", "health_price"), gt=0.0)
    education_price: float = Field(5.0, validation_alias=AliasChoices("p_e", "education_price"), gt=0.0)
    leisure_price: float = Field(10.0, validation_alias=AliasChoices("p_l", "leisure_price", "luxury_price"), gt=0.0)
    target_welfare: float = Field(2.97, validation_alias=AliasChoices("S*", "S_star", "target_welfare"), gt=0.0)
    health_budget_ratio: float = Field(0.40, validation_alias=AliasChoices("rho_h", "health_budget_ratio"), ge=0.0)
    education_budget_ratio: float = Field(0.35, validation_alias=AliasChoices("rho_e", "education_budget_ratio"), ge=0.0)
    leisure_budget_ratio: float = Field(0.25, validation_alias=AliasChoices("rho_l", "leisure_budget_ratio"), ge=0.0)
    health_weight: float = Field(0.40, validation_alias=AliasChoices("alpha_h", "health_weight"), ge=0.0)
    education_weight: float = Field(0.35, validation_alias=AliasChoices("alpha_e", "education_weight"), ge=0.0)
    leisure_weight: float = Field(0.25, validation_alias=AliasChoices("alpha_l", "leisure_weight"), ge=0.0)
    initial_guess: float = Field(600.0, ge=0.0)
    bracket_low: float = Field(0.0, ge=0.0)
    bracket_high: float = Field(5_000.0, gt=0.0)
    tolerance: float = Field(1e-7, gt=0.0, le=1e-2)
    max_iterations: int = Field(100, ge=1, le=1_000)

    @model_validator(mode="after")
    def validate_numerical_weights(self) -> "IncomeRequest":
        """Reject states that cannot feed the welfare equation."""

        if self.bracket_high <= self.bracket_low:
            raise ValueError("bracket_high must be greater than bracket_low.")
        if self.health_budget_ratio + self.education_budget_ratio + self.leisure_budget_ratio <= 0:
            raise ValueError("At least one budget ratio must be positive.")
        if self.health_weight + self.education_weight + self.leisure_weight <= 0:
            raise ValueError("At least one welfare weight must be positive.")
        return self

    def to_game_params(self) -> GameParams:
        """Convert the HTTP payload into the existing domain dataclass."""

        return GameParams(
            population=self.population,
            tax_rate=self.tax_rate,
            food_available=self.food_available,
            food_price=self.food_price,
            health_initial=self.health_initial,
            education_initial=self.education_initial,
            leisure_initial=self.leisure_initial,
            health_price=self.health_price,
            education_price=self.education_price,
            leisure_price=self.leisure_price,
            health_budget_ratio=self.health_budget_ratio,
            education_budget_ratio=self.education_budget_ratio,
            leisure_budget_ratio=self.leisure_budget_ratio,
            health_weight=self.health_weight,
            education_weight=self.education_weight,
            leisure_weight=self.leisure_weight,
            target_welfare=self.target_welfare,
            bracket_low=self.bracket_low,
            bracket_high=self.bracket_high,
            initial_guess=self.initial_guess,
            secondary_guess=max(self.initial_guess * 1.15, self.initial_guess + 1.0),
        )


app = FastAPI(
    title="Hegemony Numerical Engine API",
    description="Calcula el ingreso minimo de la Clase Trabajadora usando Newton-Raphson.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _safe_newton_params(params: GameParams, tolerance: float, max_iterations: int) -> GameParams:
    """Reuse the project's bracketing preparation, then solve only with Newton."""

    try:
        return WelfareCalculatorService(tolerance=tolerance, max_iterations=max_iterations)._prepare_params(params)
    except (NumericalMethodError, ValueError, ZeroDivisionError):
        minimum_guess = minimum_income_for_domain(params) + 1.0
        return replace(params, initial_guess=max(params.initial_guess, minimum_guess))


def _history_to_json(result: Any) -> list[dict[str, float | int | None]]:
    """Serialize Newton iteration dataclasses for React charts."""

    return [
        {
            "iteration": step.iteration,
            "estimate": step.estimate,
            "function_value": step.function_value,
            "relative_error": step.relative_error,
            "derivative_value": step.derivative_value,
        }
        for step in result.history
    ]


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Small endpoint for deployment checks."""

    return {"status": "ok"}


@app.get("/")
def api_index() -> dict[str, str]:
    """Friendly landing response when opening the API in a browser."""

    return {
        "name": "Hegemony Numerical Engine API",
        "status": "ok",
        "docs": "/docs",
        "calculate_income": "POST /api/calculate-income",
    }


@app.post("/api/calculate-income")
def calculate_income(payload: IncomeRequest) -> dict[str, Any]:
    """Calculate the minimum income I* for the current Working Class state."""

    params = payload.to_game_params()
    tuned_params = _safe_newton_params(params, payload.tolerance, payload.max_iterations)

    try:
        result = NewtonRaphsonMethod(
            tuned_params,
            tolerance=payload.tolerance,
            max_iterations=payload.max_iterations,
        ).solve()
        welfare_at_root = welfare(result.root, tuned_params)
    except (NumericalMethodError, ValueError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    food_gap = tuned_params.food_gap
    narrative = (
        f"Tus obreros necesitan al menos {result.root:.2f}V de ingreso bruto "
        f"para cubrir comida, impuestos y alcanzar la meta de Prosperidad {tuned_params.target_welfare:.2f}."
    )
    if food_gap > 0:
        narrative += f" Antes de comprar bienestar, faltan {food_gap:.0f} unidades de comida."

    return {
        "method": result.method_name,
        "I_star": result.root,
        "required_income": result.root,
        "target_welfare": tuned_params.target_welfare,
        "welfare_at_root": welfare_at_root,
        "free_budget_at_root": free_budget(result.root, tuned_params),
        "mandatory_food_cost": mandatory_food_cost(tuned_params),
        "converged": result.converged,
        "iterations": result.iterations,
        "final_error": result.final_error,
        "execution_time_ms": result.execution_time_ms,
        "message": result.message,
        "narrative": narrative,
        "history": _history_to_json(result),
        "parameters": asdict(tuned_params),
    }
