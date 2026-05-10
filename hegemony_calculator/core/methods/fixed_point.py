"""Fixed-point method implementation."""

from __future__ import annotations

from time import perf_counter

from hegemony_calculator.core.methods.base import NumericalMethod, NumericalMethodError
from hegemony_calculator.core.models import IterationStep, MethodResult
from hegemony_calculator.core.welfare import welfare_gap, welfare_gap_derivative


class FixedPointMethod(NumericalMethod):
    """Solve for the welfare root using a damped fixed-point transform."""

    method_name = "Fixed Point"

    def solve(self) -> MethodResult:
        start = perf_counter()
        current = self.params.initial_guess
        history: list[IterationStep] = []
        previous: float | None = None
        damping = self._resolve_damping_factor(current)

        for iteration in range(1, self.max_iterations + 1):
            f_current = welfare_gap(current, self.params)
            damping = self._resolve_damping_factor(current)
            next_value = current - (damping * f_current)
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
                    f"Converged with damping factor {damping:.6f}.",
                )
            previous = current
            current = next_value

            if previous is not None and abs(current - previous) <= 1e-14:
                raise NumericalMethodError("Fixed-point iteration stagnated.")

        final_error = history[-1].relative_error or abs(history[-1].function_value)
        return self.build_result(current, self.max_iterations, final_error, False, history, start, "Maximum iterations reached.")

    def _resolve_damping_factor(self, current: float) -> float:
        """Choose a stable damping factor for the fixed-point transform."""

        derivative = welfare_gap_derivative(current, self.params)
        if derivative <= 0:
            raise NumericalMethodError("Unable to determine a stable damping factor for fixed point.")
        adaptive = 0.95 / derivative
        return min(self.params.fixed_point_k, adaptive)
