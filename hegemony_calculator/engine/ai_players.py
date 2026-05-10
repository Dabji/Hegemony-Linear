"""Simple automated behavior for non-selected classes."""

from __future__ import annotations

from hegemony_calculator.core.models import ClassRole, GameState


def run_ai_turns(state: GameState) -> list[str]:
    """Apply small pressure from classes not controlled by the user."""

    messages: list[str] = []
    capitalist = state.players[ClassRole.CAPITALIST]
    middle = state.players[ClassRole.MIDDLE]
    state_player = state.players[ClassRole.STATE]

    capitalist.capital += 6
    middle.resources.vardis += 4
    state_player.legitimacy = max(0, min(10, state_player.legitimacy + 1))
    messages.append("Capitalistas reinvirtieron capital, la clase media abrio consumo y el Estado sostuvo legitimidad.")
    state.narrative_log.extend(messages)
    return messages

