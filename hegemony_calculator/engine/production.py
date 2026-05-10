"""Production and resource flow rules."""

from __future__ import annotations

from hegemony_calculator.core.models import ClassRole, GameState
from hegemony_calculator.engine.tax_calculator import working_tax_bill


WAGE_BY_LEVEL: dict[int, int] = {1: 10, 2: 15, 3: 22}
LABOR_POLICY_WAGE_LEVEL: dict[str, int] = {"A": 1, "B": 2, "C": 3}


def current_wage_level(state: GameState) -> int:
    """Return wage level derived from labor policy."""

    return LABOR_POLICY_WAGE_LEVEL[state.policies.labor_market]


def resolve_production(state: GameState) -> list[str]:
    """Run automatic production, wages, food needs, and taxes."""

    player = state.players[ClassRole.WORKING]
    wage_level = current_wage_level(state)
    wage = WAGE_BY_LEVEL[wage_level]
    employed = sum(company.assigned_workers for company in state.companies)
    player.employed_workers = min(player.population, employed)

    qualified_bonus = min(player.qualified_workers, player.employed_workers) * 4
    gross_income = (player.employed_workers * wage) + qualified_bonus
    tax_bill = min(gross_income, working_tax_bill(player.population, state.policies))
    net_income = gross_income - tax_bill

    player.resources.vardis += net_income
    state.last_income = net_income
    state.last_tax = tax_bill

    produced_messages: list[str] = []
    for company in state.companies:
        if company.assigned_workers <= 0:
            continue
        output = company.assigned_workers * company.output_amount
        current_value = getattr(player.resources, company.output_resource)
        setattr(player.resources, company.output_resource, current_value + output)
        produced_messages.append(f"{company.name} produjo {output} de {company.output_resource}.")

    if player.resources.food >= player.population:
        player.resources.food -= player.population
        food_message = f"La poblacion consumio {player.population} de comida sin crisis."
    else:
        missing = player.population - player.resources.food
        player.resources.food = 0
        player.prosperity = max(0, player.prosperity - 1)
        food_message = f"Faltaron {missing} de comida. La prosperidad bajo por presion social."

    messages = [
        f"Tus {player.employed_workers} obreros ganaron {gross_income}V brutos.",
        f"Pagaste {tax_bill}V en impuestos y recibiste {net_income}V netos.",
        *produced_messages,
        food_message,
    ]
    state.narrative_log.extend(messages)
    return messages

