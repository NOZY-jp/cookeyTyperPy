from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, TypedDict, Union


class CookieSource(Enum):
    ELSE = 1
    TYPING = 2
    FACILITY = 3
    FACILITY_PURCHASE = 4
    UPGRADE_PURCHASE = 5


class VisualState(Enum):
    SHOWN = 1
    COVERED = 2
    HIDDEN = 3


class FacilityTypes(Enum):
    KEYBOARD = auto()
    GRANDMA = auto()
    FARM = auto()
    MINE = auto()
    FACTORY = auto()
    BANK = auto()
    TEMPLE = auto()
    WIZARD_TOWER = auto()
    SHIPMENT = auto()
    ALCHEMY_LAB = auto()
    PORTAL = auto()
    TIME_MACHINE = auto()
    ANTIMATTER_CONDENSER = auto()
    PRISM = auto()
    CHANCE_MAKER = auto()
    FRACTAL_ENGINE = auto()
    PYTHON_CONSOLE = auto()
    IDLEVERSE = auto()
    CORTEX_BAKER = auto()
    YOU = auto()


class FacilityConfig(TypedDict):
    name: str
    description: str
    base_cost: int
    base_cps: float | int
    init_visual: VisualState


class UpgradeTypes(Enum):
    REINFORCED_INDEX_FINGER = auto()


class Res(Enum):
    OK = 1
    ERR = 2


class ModifierSourceType(Enum):
    UPGRADE = auto()


class Parameters(TypedDict):
    facility_cost_multiplier_by_amount: float
    tick_rate: int


# ----------   Commands   ----------


class Operations(Enum):
    INVALID_OPERATION_ERROR = 1
    BUY = 2
    SELL = 3
    DETAIL = 4
    LS = 5
    LA = 6


@dataclass
class CommandInvalidError:
    type: Literal["invalid"] = "invalid"


@dataclass
class CommandFacility:
    operation: Operations
    target: FacilityTypes | None = None
    type: Literal["facility"] = "facility"
    amount: int = 1


@dataclass
class CommandUpgrade:
    operation: Operations
    target: UpgradeTypes | None = None
    type: Literal["upgrade"] = "upgrade"


@dataclass
class CommandHelp:
    type: Literal["help"] = "help"


@dataclass
class CommandInspectCookieCount:
    type: Literal["cc"] = "cc"


@dataclass
class CommandInspectCookiePerSecond:
    type: Literal["cps"] = "cps"


@dataclass
class CommandInspectCookiePerType:
    type: Literal["cpt"] = "cpt"


@dataclass
class CommandUserInput:
    type: Literal["input"] = "input"
    content: str = ""


Command = Union[
    CommandInvalidError,
    CommandFacility,
    CommandUpgrade,
    CommandHelp,
    CommandInspectCookieCount,
    CommandInspectCookiePerSecond,
    CommandInspectCookiePerType,
    CommandUserInput,
]
