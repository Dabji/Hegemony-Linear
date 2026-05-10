"""Secant method implementation."""

from __future__ import annotations

from time import perf_counter

from hegemony_calculator.core.methods.base import NumericalMethod, NumericalMethodError
from hegemony_calculator.core.models import IterationStep, MethodResult
from hegemony_calculator.core.welfare import welfare_gap


class SecantMethod(NumericalMethod):
    """Solve for the welfare root using the secant method."""

    method_name = "Secant"

    def solve(self) -> MethodResult:
        start = perf_counter()
        previous = self.params.initial_guess
        current = self.params.secondary_guess
        history: list[IterationStep] = []

        for iteration in range(1, self.max_iterations + 1):
            f_previous = welfare_gap(previous, self.params)
            f_current = welfare_gap(current, self.params)
            denominator = f_previous - f_current
            if denominator == 0:
                raise NumericalMethodError("Secant method encountered division by zero.")

            next_value = current - (f_current * (previous - current) / denominator)
            error = self.relative_error(next_value, current)
            history.append(
                IterationStep(
                    iteration=iteration,
                    estimate=next_value,
                    function_value=welfare_gap(next_value, self.params),
                    relative_error=error,
                )
            )

            if abs(history[-1].function_value) <= self.tolerance or (error is not None and error <= self.tolerance):
                return self.build_result(
                    next_value,
                    iteration,
                    error or 0.0,
                    True,
                    history,
                    start,
                    "Converged successfully.",
                )

            previous, current = current, next_value

        final_error = history[-1].relative_error or abs(history[-1].function_value)
        return self.build_result(current, self.max_iterations, final_error, False, history, start, "Maximum iterations reached.")

