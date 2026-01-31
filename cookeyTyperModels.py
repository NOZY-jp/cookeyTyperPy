from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import TYPE_CHECKING, Callable, Literal

from cookeyTyperData import facilities, parameters
from cookeyTyperTypes import (
    EffectType,
    FacilityTypes,
    ModifierSourceType,
    UpgradeTypes,
    VisualState,
)
from result import Err, Ok, Result, is_ok

if TYPE_CHECKING:
    from cookeyTyperCore import CookeyTyper


type EffectTarget = FacilityTypes | Literal["Global"] | Literal["Click"]


@dataclass(frozen=True, slots=True)
class Modifier:
    source_type: ModifierSourceType
    source_id: UpgradeTypes
    effect_type: EffectType
    value: float


@dataclass(frozen=True, slots=True)
class Effect[T: EffectTarget]:
    target: T
    effect_type: EffectType
    value: float


@dataclass
class Upgrade:
    type: UpgradeTypes
    name: str
    description: str
    price: int
    effects: list[Effect[EffectTarget]]
    unlock_condition: Callable[[CookeyTyper], bool]
    is_purchased: bool = False


class Facility:
    def __init__(
        self,
        facility_type: FacilityTypes,
        name: str,
        description: str,
        base_cost: int,
        base_cps: int | float,
        init_visual: VisualState,
    ) -> None:
        self.type: FacilityTypes = facility_type
        self.name: str = name
        self.description: str = description
        self.base_cost: int = base_cost
        self.base_cps: float = float(base_cps)
        self.visual_state: VisualState = init_visual
        self.amount: int = 0
        self.modifiers: list[Modifier] = []

    def add_modifier(self, mod: Modifier) -> bool:
        if mod.source_type == ModifierSourceType.UPGRADE:
            for existing in self.modifiers:
                if (
                    existing.source_type == ModifierSourceType.UPGRADE
                    and existing.source_id == mod.source_id
                ):
                    return False
        self.modifiers.append(mod)
        return True

    @property
    def cps(self) -> float:
        base = self.base_cps

        add_total: float = 0.0
        mult_total: float = 1.0

        for mod in self.modifiers:
            if mod.effect_type == EffectType.ADD:
                add_total += mod.value
            elif mod.effect_type == EffectType.MULTIPLIER:
                mult_total *= mod.value

        return (base + add_total) * mult_total * self.amount

    def next_cost(self) -> int:
        next_cost = self.get_cookie_delta(1)
        if is_ok(next_cost):
            next_cost = abs(next_cost.value)
            return next_cost
        else:
            print("-" * 50)
            print("[CRITICAL ERROR] Next cost was calculated incorrectly")
            print("This should NOT happen if the cost calculater is working correctly")
            print("Please report this bug to the author with your input.")
            print("-" * 50)
            return 0

    def get_cookie_delta(
        self, diff_amount: int = 1, base_amount: int | None = None
    ) -> Result[int, int]:
        ratio = parameters()["facility_cost_multiplier_by_amount"]
        if base_amount is None:
            base_amount = self.amount

        if diff_amount == 0:
            return Ok(0)

        result = True
        if base_amount + diff_amount < 0:
            diff_amount = -base_amount
            result = False

        raw_total = (
            self.base_cost
            * (pow(ratio, base_amount + diff_amount) - pow(ratio, base_amount))
        ) / (ratio - 1)

        if diff_amount > 0:
            final_cost = -int(ceil(raw_total))
        else:
            final_cost = int(abs(ceil(raw_total)) * 0.5)

        if result:
            return Ok(final_cost)
        else:
            return Err(final_cost)

    def delta_amount(self, amount: int = 1) -> bool:
        if amount < 0:
            if self.amount < abs(amount):
                print(f"You only have {self.amount} {self.name}(s)")
                return False
        self.amount += amount
        return True


def get_facilities() -> dict[FacilityTypes, Facility]:
    facilities_dict: dict[FacilityTypes, Facility] = {}
    for facility_type, config in facilities().items():
        facilities_dict[facility_type] = Facility(
            facility_type=facility_type,
            name=config["name"],
            description=config["description"],
            base_cost=config["base_cost"],
            base_cps=config["base_cps"],
            init_visual=config["init_visual"],
        )
    return facilities_dict


def into_facility(arg: str) -> Result[FacilityTypes, str]:
    for facility, config in facilities().items():
        if config["name"].lower() == arg.lower():
            return Ok(facility)
    return Err("Invalid Facility Name")


def into_upgrade(arg: str) -> Result[UpgradeTypes, str]:
    from cookeyTyperData import upgrades

    # Normalize user input: lowercase, replace spaces/hyphens with underscores
    normalized_arg = arg.lower().replace(" ", "_").replace("-", "_")

    for upgrade_type, config in upgrades().items():
        name = config["name"].lower().replace(" ", "_").replace("-", "_")
        if name == normalized_arg or upgrade_type.name.lower() == normalized_arg:
            return Ok(upgrade_type)
    return Err("Invalid Upgrade Name")
