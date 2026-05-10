"""Election system with cube draws and influence."""

from __future__ import annotations

import random

from hegemony_calculator.core.models import ClassRole, ElectionProposal, GameState


CUBE_BAG: tuple[ClassRole, ...] = (
    ClassRole.WORKING,
    ClassRole.WORKING,
    ClassRole.WORKING,
    ClassRole.MIDDLE,
    ClassRole.MIDDLE,
    ClassRole.CAPITALIST,
    ClassRole.CAPITALIST,
    ClassRole.STATE,
    ClassRole.STATE,
)


def create_worker_welfare_proposal(state: GameState) -> ElectionProposal:
    """Create a default worker-friendly public health proposal."""

    return ElectionProposal(
        proposer=ClassRole.WORKING,
        policy_key="public_health",
        target_level="A",
        title="Salud publica universal",
    )


def resolve_election(state: GameState, influence_spent: int = 0) -> list[str]:
    """Resolve a pending election proposal."""

    proposal = state.election_proposal or create_worker_welfare_proposal(state)
    player = state.players[ClassRole.WORKING]
    spend = min(influence_spent, player.resources.influence)
    player.resources.influence -= spend
    proposal.influence_spent = spend

    rng = random.Random((state.round_number * 100) + state.turn_number + spend)
    drawn = [rng.choice(CUBE_BAG) for _ in range(5)]
    worker_votes = sum(1 for cube in drawn if cube in {ClassRole.WORKING, ClassRole.STATE})
    opposition_votes = len(drawn) - worker_votes
    worker_votes += spend
    passed = worker_votes > opposition_votes

    if passed:
        setattr(state.policies, proposal.policy_key, proposal.target_level)
        player.victory_points += 3
        outcome = f"La ley '{proposal.title}' fue aprobada: {worker_votes} a {opposition_votes}."
    else:
        outcome = f"La ley '{proposal.title}' fue rechazada: {worker_votes} a {opposition_votes}."

    cube_text = ", ".join(cube.value for cube in drawn)
    messages = [f"Cubos extraidos: {cube_text}.", outcome]
    state.election_proposal = None
    state.narrative_log.extend(messages)
    return messages

