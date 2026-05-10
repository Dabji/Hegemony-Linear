"""Tests for policy-driven taxes."""

from __future__ import annotations

from hegemony_calculator.core.models import Policies
from hegemony_calculator.engine.tax_calculator import effective_tax_rate, working_tax_bill, working_tax_per_population


def test_working_tax_table_matches_policy_positions() -> None:
    policies = Policies(labor_market="A", taxation="B")
    assert working_tax_per_population(policies) == 6
    assert working_tax_bill(10, policies) == 60


def test_effective_tax_rate_is_bounded() -> None:
    policies = Policies(labor_market="A", taxation="A")
    assert effective_tax_rate(100.0, 10, policies) == 0.55

