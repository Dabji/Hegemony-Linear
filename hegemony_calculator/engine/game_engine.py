"""Main game orchestration."""

from __future__ import annotations

from hegemony_calculator.core.models import ClassRole, Company, GamePhase, GameState, Player, Resources
from hegemony_calculator.engine.ai_players import run_ai_turns
from hegemony_calculator.engine.elections import create_worker_welfare_proposal, resolve_election
from hegemony_calculator.engine.income_solver import solve_income_need
from hegemony_calculator.engine.production import resolve_production


PHASE_ORDER: tuple[GamePhase, ...] = (
    GamePhase.PREPARATION,
    GamePhase.ACTION,
    GamePhase.PRODUCTION,
    GamePhase.ELECTIONS,
    GamePhase.SCORING,
)


def new_game(active_role: ClassRole = ClassRole.WORKING, players_count: int = 1) -> GameState:
    """Create a new game state."""

    players = {
        ClassRole.WORKING: Player(
            role=ClassRole.WORKING,
            victory_points=0,
            resources=Resources(vardis=42, food=6, health=0, education=0, luxury=0, influence=3),
            population=10,
            employed_workers=5,
            qualified_workers=1,
            prosperity=2,
            prosperity_goal=4,
        ),
        ClassRole.MIDDLE: Player(role=ClassRole.MIDDLE, victory_points=0, resources=Resources(vardis=35, influence=2)),
        ClassRole.CAPITALIST: Player(role=ClassRole.CAPITALIST, victory_points=0, resources=Resources(vardis=60, influence=2), capital=65),
        ClassRole.STATE: Player(role=ClassRole.STATE, victory_points=0, resources=Resources(vardis=50, influence=2), legitimacy=6),
    }
    companies = [
        Company("farm_1", "Cooperativa Agricola", "Agricultura", ClassRole.MIDDLE, 3, 2, 2, "food", 2),
        Company("farm_2", "Agroholding Verde", "Agricultura", ClassRole.CAPITALIST, 4, 2, 2, "food", 3),
        Company("clinic_1", "Clinica Publica", "Salud", ClassRole.STATE, 3, 1, 2, "health", 2, True),
        Company("school_1", "Instituto Publico", "Educacion", ClassRole.STATE, 3, 0, 2, "education", 2, True),
        Company("media_1", "Canal Popular", "Media", ClassRole.MIDDLE, 2, 0, 2, "influence", 1),
        Company("lux_1", "Distrito de Ocio", "Ocio", ClassRole.CAPITALIST, 3, 0, 2, "luxury", 2),
    ]
    state = GameState(active_role=active_role, players_count=players_count, players=players, companies=companies)
    state.narrative_log.append("La partida empieza con la Clase Trabajadora buscando prosperar sin ver el motor matematico.")
    solve_income_need(state, actual_income=0)
    return state


def set_prosperity_goal(state: GameState, goal: int) -> None:
    """Set the worker prosperity target."""

    player = state.players[ClassRole.WORKING]
    player.prosperity_goal = max(player.prosperity + 1, min(10, goal))
    solve_income_need(state)


def assign_worker(state: GameState) -> str:
    """Assign one unemployed worker to the best open company."""

    player = state.players[ClassRole.WORKING]
    open_companies = [company for company in state.companies if company.open_slots > 0]
    if player.employed_workers >= player.population or not open_companies:
        message = "No quedan obreros libres o espacios de trabajo disponibles."
        state.narrative_log.append(message)
        return message

    target = sorted(open_companies, key=lambda company: (company.wage_level, company.output_amount), reverse=True)[0]
    target.assigned_workers += 1
    player.employed_workers += 1
    message = f"Un obrero fue asignado a {target.name}. La presion salarial mejora tu produccion futura."
    state.narrative_log.append(message)
    solve_income_need(state)
    return message


def buy_and_use_resource(state: GameState, resource: str) -> str:
    """Buy the population-sized bundle of a prosperity resource and use it."""

    player = state.players[ClassRole.WORKING]
    costs = {"health": 5, "education": 5, "luxury": 10, "food": 4}
    labels = {"health": "Salud", "education": "Educacion", "luxury": "Ocio", "food": "Comida"}
    amount = player.population
    total_cost = amount * costs[resource]

    if player.resources.vardis < total_cost:
        message = f"No hay suficientes Vardis para comprar {labels[resource]} para toda la poblacion."
        state.narrative_log.append(message)
        return message

    player.resources.vardis -= total_cost
    current_value = getattr(player.resources, resource)
    setattr(player.resources, resource, current_value + amount)

    if resource == "food":
        message = f"Compraste {amount} de Comida. La necesidad basica queda mejor cubierta."
    else:
        setattr(player.resources, resource, getattr(player.resources, resource) - amount)
        player.prosperity = min(10, player.prosperity + 1)
        player.victory_points += player.prosperity
        if resource == "health":
            player.victory_points += 2
            player.population += 1
            extra = " Ademas llega un nuevo obrero gris."
        elif resource == "education":
            player.qualified_workers += 1
            extra = " Un obrero mejora a calificado."
        else:
            extra = " La vida cotidiana se vuelve mas respirable."
        message = f"Usaste {labels[resource]} y subiste a Prosperidad {player.prosperity}.{extra}"

    state.narrative_log.append(message)
    solve_income_need(state)
    return message


def strike(state: GameState) -> str:
    """Perform a strike for influence and pressure."""

    player = state.players[ClassRole.WORKING]
    player.resources.influence += 2
    player.victory_points += 1
    message = "La huelga suma 2 de Influencia y empuja el debate salarial."
    state.narrative_log.append(message)
    solve_income_need(state)
    return message


def propose_law(state: GameState) -> str:
    """Create a worker-friendly policy proposal."""

    state.election_proposal = create_worker_welfare_proposal(state)
    state.phase = GamePhase.ELECTIONS
    message = "Propusiste Salud publica universal. La eleccion se prepara con cubos e influencia."
    state.narrative_log.append(message)
    return message


def advance_phase(state: GameState) -> list[str]:
    """Advance to the next phase and run automatic effects."""

    current_index = PHASE_ORDER.index(state.phase)
    next_index = (current_index + 1) % len(PHASE_ORDER)
    if next_index == 0:
        state.round_number += 1
        state.turn_number = 1
        if state.round_number > 5:
            state.game_over = True
            message = "La quinta ronda termina. El pais queda marcado por tus decisiones."
            state.narrative_log.append(message)
            return [message]

    state.phase = PHASE_ORDER[next_index]
    messages = [f"Avanza la fase: {state.phase.value}."]

    if state.phase == GamePhase.PREPARATION:
        immigrant_gain = {"A": 0, "B": 1, "C": 2}[state.policies.immigration]
        state.players[ClassRole.WORKING].population += immigrant_gain
        messages.append(f"Llegan {immigrant_gain} nuevos obreros por politica migratoria.")
    elif state.phase == GamePhase.PRODUCTION:
        messages.extend(resolve_production(state))
        solve_income_need(state)
    elif state.phase == GamePhase.ELECTIONS and state.election_proposal is None:
        messages.append(propose_law(state))
    elif state.phase == GamePhase.SCORING:
        messages.extend(score_round(state))
        messages.extend(run_ai_turns(state))

    state.narrative_log.extend(messages)
    return messages


def resolve_current_election(state: GameState, influence_spent: int) -> list[str]:
    """Resolve election phase with selected influence spend."""

    return resolve_election(state, influence_spent)


def score_round(state: GameState) -> list[str]:
    """Score the current round."""

    player = state.players[ClassRole.WORKING]
    round_points = player.prosperity + player.unions * 2
    player.victory_points += round_points
    messages = [f"Puntuacion: Prosperidad {player.prosperity} otorga {round_points} PV esta ronda."]
    if player.prosperity >= player.prosperity_goal:
        player.victory_points += 2
        messages.append("La meta de prosperidad se cumplio y ganas 2 PV extra.")
    return messages

