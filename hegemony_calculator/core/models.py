"""Domain models for the Hegemony calculator."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Optional

from hegemony_calculator.config import DEFAULT_BRACKET, DEFAULT_FIXED_POINT_K, DEFAULT_SECANT_GUESS


@dataclass(slots=True)
class GameParams:
    """Input parameters for one worker-class welfare simulation round."""

    population: int
    tax_rate: float
    food_available: float
    food_price: float
    health_initial: float
    education_initial: float
    leisure_initial: float
    health_price: float
    education_price: float
    leisure_price: float
    health_budget_ratio: float
    education_budget_ratio: float
    leisure_budget_ratio: float
    health_weight: float
    education_weight: float
    leisure_weight: float
    target_welfare: float
    fixed_point_k: float = DEFAULT_FIXED_POINT_K
    bracket_low: float = DEFAULT_BRACKET[0]
    bracket_high: float = DEFAULT_BRACKET[1]
    initial_guess: float = DEFAULT_SECANT_GUESS[0]
    secondary_guess: float = DEFAULT_SECANT_GUESS[1]

    @property
    def food_gap(self) -> float:
        """Return missing food units that must be purchased."""

        return max(0.0, float(self.population) - self.food_available)

    @property
    def food_cost(self) -> float:
        """Return mandatory food expenditure."""

        return self.food_gap * self.food_price


@dataclass(slots=True)
class IterationStep:
    """Single iteration snapshot for a numerical method."""

    iteration: int
    estimate: float
    function_value: float
    relative_error: Optional[float]
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    derivative_value: Optional[float] = None


@dataclass(slots=True)
class MethodResult:
    """Result of applying one numerical method."""

    method_name: str
    root: float
    iterations: int
    final_error: float
    converged: bool
    history: list[IterationStep] = field(default_factory=list)
    execution_time_ms: float = 0.0
    message: str = ""


class ClassRole(str, Enum):
    """Playable social classes."""

    WORKING = "Working Class"
    MIDDLE = "Middle Class"
    CAPITALIST = "Capitalist Class"
    STATE = "The State"


class GamePhase(str, Enum):
    """Round phases."""

    PREPARATION = "Preparacion"
    ACTION = "Accion"
    PRODUCTION = "Produccion"
    ELECTIONS = "Elecciones"
    SCORING = "Puntuacion"


PolicyLevel = Literal["A", "B", "C"]
ResourceName = Literal["vardis", "food", "health", "education", "luxury", "influence"]


@dataclass(slots=True)
class Resources:
    """Player resources."""

    vardis: int = 35
    food: int = 4
    health: int = 0
    education: int = 0
    luxury: int = 0
    influence: int = 2


@dataclass(slots=True)
class Player:
    """State for one class player."""

    role: ClassRole
    victory_points: int = 0
    resources: Resources = field(default_factory=Resources)
    population: int = 10
    employed_workers: int = 5
    qualified_workers: int = 1
    prosperity: int = 2
    prosperity_goal: int = 4
    capital: int = 45
    legitimacy: int = 6
    unions: int = 0


@dataclass(slots=True)
class Company:
    """Company card on the board."""

    company_id: str
    name: str
    industry: str
    owner: ClassRole
    worker_slots: int
    assigned_workers: int
    wage_level: int
    output_resource: ResourceName
    output_amount: int
    is_public: bool = False

    @property
    def open_slots(self) -> int:
        """Return the number of empty worker slots."""

        return max(0, self.worker_slots - self.assigned_workers)


@dataclass(slots=True)
class Policies:
    """Current policy board positions."""

    fiscal: PolicyLevel = "B"
    labor_market: PolicyLevel = "B"
    taxation: PolicyLevel = "B"
    public_health: PolicyLevel = "B"
    public_education: PolicyLevel = "B"
    foreign_trade: PolicyLevel = "B"
    immigration: PolicyLevel = "B"


@dataclass(slots=True)
class ElectionProposal:
    """Pending policy vote."""

    proposer: ClassRole
    policy_key: str
    target_level: PolicyLevel
    title: str
    influence_spent: int = 0


@dataclass(slots=True)
class NumericEngineSnapshot:
    """Hidden numerical evidence for the instructor panel."""

    required_income: float
    actual_income: float
    target_welfare: float
    results: list[MethodResult]
    narrative: str


@dataclass(slots=True)
class GameState:
    """Full mutable game state."""

    active_role: ClassRole = ClassRole.WORKING
    players_count: int = 1
    round_number: int = 1
    turn_number: int = 1
    phase: GamePhase = GamePhase.ACTION
    players: dict[ClassRole, Player] = field(default_factory=dict)
    companies: list[Company] = field(default_factory=list)
    policies: Policies = field(default_factory=Policies)
    election_proposal: ElectionProposal | None = None
    last_income: int = 0
    last_tax: int = 0
    last_numeric_snapshot: NumericEngineSnapshot | None = None
    narrative_log: list[str] = field(default_factory=list)
    game_over: bool = False

    @property
    def active_player(self) -> Player:
        """Return the selected player."""

        return self.players[self.active_role]
