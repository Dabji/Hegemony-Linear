"""False position method implementation."""

from __future__ import annotations

from time import perf_counter

from hegemony_calculator.core.methods.base import NumericalMethod, NumericalMethodError
from hegemony_calculator.core.models import IterationStep, MethodResult
from hegemony_calculator.core.welfare import welfare_gap


class FalsePositionMethod(NumericalMethod):
    """Solve for the welfare root using the false position method."""

    method_name = "False Position"

    def solve(self) -> MethodResult:
        start = perf_counter()
        lower = self.params.bracket_low
        upper = self.params.bracket_high
        f_lower = welfare_gap(lower, self.params)
        f_upper = welfare_gap(upper, self.params)

        if f_lower * f_upper > 0:
            raise NumericalMethodError("False position requires a valid bracketing interval.")

        history: list[IterationStep] = []
        previous_estimate: float | None = None
        estimate = lower

        for iteration in range(1, self.max_iterations + 1):
            denominator = f_lower - f_upper
            if denominator == 0:
                raise NumericalMethodError("Division by zero encountered in false position.")

            estimate = upper - (f_upper * (lower - upper) / denominator)
            f_estimate = welfare_gap(estimate, self.params)
            error = self.relative_error(estimate, previous_estimate)
            history.append(
                IterationStep(
                    iteration=iteration,
                    estimate=estimate,
                    function_value=f_estimate,
                    relative_error=error,
                    lower_bound=lower,
                    upper_bound=upper,
                )
            )

            if abs(f_estimate) <= self.tolerance or (error is not None and error <= self.tolerance):
                return self.build_result(
                    estimate,
                    iteration,
                    error or 0.0,
                    True,
                    history,
                    start,
                    "Converged successfully.",
                )

            if f_lower * f_estimate < 0:
                upper = estimate
                f_upper = f_estimate
            else:
                lower = estimate
                f_lower = f_estimate
            previous_estimate = estimate

        final_error = history[-1].relative_error or abs(history[-1].function_value)
        return self.build_result(estimate, self.max_iterations, final_error, False, history, start, "Maximum iterations reached.")

