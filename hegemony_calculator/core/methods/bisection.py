"""Bisection method implementation."""

from __future__ import annotations

from time import perf_counter

from hegemony_calculator.core.methods.base import NumericalMethod, NumericalMethodError
from hegemony_calculator.core.models import IterationStep, MethodResult
from hegemony_calculator.core.welfare import welfare_gap


class BisectionMethod(NumericalMethod):
    """Solve for the welfare root using the bisection method."""

    method_name = "Bisection"

    def solve(self) -> MethodResult:
        start = perf_counter()
        lower = self.params.bracket_low
        upper = self.params.bracket_high
        f_lower = welfare_gap(lower, self.params)
        f_upper = welfare_gap(upper, self.params)

        if f_lower == 0:
            return self.build_result(lower, 0, 0.0, True, [], start, "Exact lower bound root.")
        if f_upper == 0:
            return self.build_result(upper, 0, 0.0, True, [], start, "Exact upper bound root.")
        if f_lower * f_upper > 0:
            raise NumericalMethodError("Bisection requires a valid bracketing interval.")

        history: list[IterationStep] = []
        previous_midpoint: float | None = None
        midpoint = lower

        for iteration in range(1, self.max_iterations + 1):
            midpoint = (lower + upper) / 2.0
            f_mid = welfare_gap(midpoint, self.params)
            error = self.relative_error(midpoint, previous_midpoint)
            history.append(
                IterationStep(
                    iteration=iteration,
                    estimate=midpoint,
                    function_value=f_mid,
                    relative_error=error,
                    lower_bound=lower,
                    upper_bound=upper,
                )
            )
            if abs(f_mid) <= self.tolerance or (error is not None and error <= self.tolerance):
                return self.build_result(
                    midpoint,
                    iteration,
                    error or 0.0,
                    True,
                    history,
                    start,
                    "Converged successfully.",
                )

            if f_lower * f_mid < 0:
                upper = midpoint
                f_upper = f_mid
            else:
                lower = midpoint
                f_lower = f_mid
            previous_midpoint = midpoint

        final_error = history[-1].relative_error or abs(history[-1].function_value)
        return self.build_result(midpoint, self.max_iterations, final_error, False, history, start, "Maximum iterations reached.")

