"""Base abstractions and utilities for numerical methods."""

from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Optional

from hegemony_calculator.config import DEFAULT_MAX_ITERATIONS, DEFAULT_TOLERANCE
from hegemony_calculator.core.models import GameParams, IterationStep, MethodResult


class NumericalMethodError(Exception):
    """Raised when a numerical method cannot proceed safely."""


class NumericalMethod(ABC):
    """Abstract base class for all root-finding methods."""

    method_name: str

    def __init__(
        self,
        params: GameParams,
        tolerance: float = DEFAULT_TOLERANCE,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ) -> None:
        self.params = params
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    @abstractmethod
    def solve(self) -> MethodResult:
        """Execute the numerical method and return a typed result."""

    def build_result(
        self,
        root: float,
        iterations: int,
        final_error: float,
        converged: bool,
        history: list[IterationStep],
        start_time: float,
        message: str = "",
    ) -> MethodResult:
        """Create a standardized method result."""

        elapsed_ms = (perf_counter() - start_time) * 1000.0
        return MethodResult(
            method_name=self.method_name,
            root=root,
            iterations=iterations,
            final_error=final_error,
            converged=converged,
            history=history,
            execution_time_ms=elapsed_ms,
            message=message,
        )

    @staticmethod
    def relative_error(current: float, previous: Optional[float]) -> Optional[float]:
        """Compute relative error between consecutive estimates."""

        if previous is None:
            return None
        denominator = max(abs(current), 1e-12)
        return abs(current - previous) / denominator

