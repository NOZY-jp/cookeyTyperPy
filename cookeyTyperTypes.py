from dataclasses import dataclass
from enum import Enum
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
    KEYBOARD = 1
    GRANDMA = 2
    FARM = 3
    MINE = 4
    FACTORY = 5
    BANK = 6
    TEMPLE = 7
    WIZARD_TOWER = 8
    SHIPMENT = 9
    ALCHEMY_LAB = 10
    PORTAL = 11
    TIME_MACHINE = 12
    ANTIMATTER_CONDENSER = 13
    PRISM = 14
    CHANCE_MAKER = 15
    FRACTAL_ENGINE = 16
    PYTHON_CONSOLE = 17
    IDLEVERSE = 18
    CORTEX_BAKER = 19
    YOU = 20


class FacilityConfig(TypedDict):
    name: str
    description: str
    base_cost: int
    base_cps: float | int
    init_visual: VisualState


class UpgradeTypes(Enum):
    REINFORCED_INDEX_FINGER = 1


class Res(Enum):
    OK = 1
    ERR = 2


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
