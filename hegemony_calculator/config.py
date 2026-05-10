"""Application-wide configuration constants."""

from __future__ import annotations

DEFAULT_TOLERANCE: float = 1e-6
DEFAULT_MAX_ITERATIONS: int = 100
DEFAULT_FIXED_POINT_K: float = 10_000.0
DEFAULT_BRACKET: tuple[float, float] = (0.0, 10_000.0)
DEFAULT_SECANT_GUESS: tuple[float, float] = (100.0, 500.0)
CLASS_OPTIONS: tuple[str, ...] = (
    "Working Class",
    "Middle Class",
    "Capitalist Class",
    "The State",
)
