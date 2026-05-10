"""Application service that orchestrates all numerical methods."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from hegemony_calculator.config import DEFAULT_MAX_ITERATIONS, DEFAULT_TOLERANCE
from hegemony_calculator.core.methods import (
    BisectionMethod,
    FalsePositionMethod,
    FixedPointMethod,
    NewtonRaphsonMethod,
    SecantMethod,
)
from hegemony_calculator.core.methods.base import NumericalMethodError
from hegemony_calculator.core.models import GameParams, MethodResult
from hegemony_calculator.core.welfare import welfare_gap


@dataclass(slots=True)
class CalculationSummary:
    """Aggregated results returned by the calculator service."""

    results: list[MethodResult]
    comparison_table: pd.DataFrame
    consensus_root: float | None
    effective_params: GameParams


class WelfareCalculatorService:
    """Run every numerical method and assemble a comparison summary."""

    def __init__(
        self,
        tolerance: float = DEFAULT_TOLERANCE,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ) -> None:
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def solve_all(self, params: GameParams) -> CalculationSummary:
        """Execute all five numerical methods for the same welfare equation."""

        tuned_params = self._prepare_params(params)
        methods = [
            BisectionMethod(tuned_params, self.tolerance, self.max_iterations),
            FalsePositionMethod(tuned_params, self.tolerance, self.max_iterations),
            FixedPointMethod(tuned_params, self.tolerance, self.max_iterations),
            NewtonRaphsonMethod(tuned_params, self.tolerance, self.max_iterations),
            SecantMethod(tuned_params, self.tolerance, self.max_iterations),
        ]

        results: list[MethodResult] = []
        for method in methods:
            try:
                results.append(method.solve())
            except (NumericalMethodError, ValueError, ZeroDivisionError) as exc:
                results.append(
                    MethodResult(
                        method_name=method.method_name,
                        root=float("nan"),
                        iterations=0,
                        final_error=float("inf"),
                        converged=False,
                        history=[],
                        execution_time_ms=0.0,
                        message=str(exc),
                    )
                )

        comparison = pd.DataFrame(
            [
                {
                    "Method": result.method_name,
                    "I*": result.root,
                    "Iterations": result.iterations,
                    "Final Error": result.final_error,
                    "Time (ms)": result.execution_time_ms,
                    "Converged": result.converged,
                    "Message": result.message,
                }
                for result in results
            ]
        )
        converged_roots = [result.root for result in results if result.converged]
        consensus_root = sum(converged_roots) / len(converged_roots) if converged_roots else None
        return CalculationSummary(
            results=results,
            comparison_table=comparison,
            consensus_root=consensus_root,
            effective_params=tuned_params,
        )

    def _prepare_params(self, params: GameParams) -> GameParams:
        """Tune intervals and guesses so every method starts from safe values."""

        lower, upper = self._find_valid_bracket(params.bracket_low, params.bracket_high, params)
        seed_lower = lower
        seed_upper = upper
        f_seed_lower = welfare_gap(seed_lower, params)
        for _ in range(8):
            midpoint = (seed_lower + seed_upper) / 2.0
            f_midpoint = welfare_gap(midpoint, params)
            if f_seed_lower * f_midpoint <= 0:
                seed_upper = midpoint
            else:
                seed_lower = midpoint
                f_seed_lower = f_midpoint

        initial_guess = (seed_lower + seed_upper) / 2.0
        span = max(seed_upper - seed_lower, 1.0)
        secondary_guess = min(seed_upper - 1e-6, initial_guess + (0.20 * span))
        if abs(secondary_guess - initial_guess) <= 1e-9:
            secondary_guess = max(seed_lower + 1e-6, initial_guess - (0.20 * span))

        return GameParams(
            population=params.population,
            tax_rate=params.tax_rate,
            food_available=params.food_available,
            food_price=params.food_price,
            health_initial=params.health_initial,
            education_initial=params.education_initial,
            leisure_initial=params.leisure_initial,
            health_price=params.health_price,
            education_price=params.education_price,
            leisure_price=params.leisure_price,
            health_budget_ratio=params.health_budget_ratio,
            education_budget_ratio=params.education_budget_ratio,
            leisure_budget_ratio=params.leisure_budget_ratio,
            health_weight=params.health_weight,
            education_weight=params.education_weight,
            leisure_weight=params.leisure_weight,
            target_welfare=params.target_welfare,
            fixed_point_k=params.fixed_point_k,
            bracket_low=lower,
            bracket_high=upper,
            initial_guess=initial_guess,
            secondary_guess=secondary_guess,
        )

    def _find_valid_bracket(self, lower: float, upper: float, params: GameParams) -> tuple[float, float]:
        """Expand the initial interval until it brackets the welfare root."""

        from hegemony_calculator.core.welfare import minimum_income_for_domain

        current_lower = max(lower, minimum_income_for_domain(params))
        current_upper = upper
        f_lower = welfare_gap(current_lower, params)
        f_upper = welfare_gap(current_upper, params)
        expansion_count = 0

        while f_lower * f_upper > 0 and expansion_count < 25:
            current_upper *= 1.5
            f_upper = welfare_gap(current_upper, params)
            expansion_count += 1

        if f_lower * f_upper > 0:
            raise NumericalMethodError("Could not find a valid interval that brackets the welfare root.")
        return current_lower, current_upper
