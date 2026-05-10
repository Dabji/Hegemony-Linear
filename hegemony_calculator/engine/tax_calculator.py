"""Policy-driven tax calculations."""

from __future__ import annotations

from hegemony_calculator.core.models import Policies


WORKING_CLASS_TAX_TABLE: dict[str, dict[str, int]] = {
    "A": {"A": 7, "B": 6, "C": 5},
    "B": {"A": 4, "B": 4, "C": 4},
    "C": {"A": 1, "B": 2, "C": 3},
}


def working_tax_per_population(policies: Policies) -> int:
    """Return worker income tax in Vardis per population marker."""

    return WORKING_CLASS_TAX_TABLE[policies.labor_market][policies.taxation]


def working_tax_bill(population: int, policies: Policies) -> int:
    """Return total worker tax bill."""

    return population * working_tax_per_population(policies)


def effective_tax_rate(gross_income: float, population: int, policies: Policies) -> float:
    """Return a bounded tax rate usable by the welfare equation."""

    if gross_income <= 0:
        return 0.35
    return min(0.55, max(0.0, working_tax_bill(population, policies) / gross_income))

