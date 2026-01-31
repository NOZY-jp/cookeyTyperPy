from __future__ import annotations

from typing import TYPE_CHECKING

from cookeyTyperData import upgrades
from cookeyTyperModels import Effect, Modifier, Upgrade
from cookeyTyperTypes import (
    CookieSource,
    EffectType,
    FacilityTypes,
    ModifierSourceType,
    UpgradeTypes,
    VisualState,
)

if TYPE_CHECKING:
    from cookeyTyperCore import CookeyTyper


def create_upgrade_from_config(
    upgrade_type: UpgradeTypes, engine: CookeyTyper
) -> Upgrade:
    config = upgrades()[upgrade_type]
    target = config["target"]
    effect = Effect(
        target=target, effect_type=config["effect_type"], value=config["value"]
    )

    unlock_facility = config["unlock_facility"]
    unlock_count = config["unlock_count"]

    def unlock_condition(e: CookeyTyper) -> bool:
        facility = e.facilities.get(unlock_facility)
        if facility is None:
            return False
        return facility.amount >= unlock_count

    return Upgrade(
        type=upgrade_type,
        name=config["name"],
        description=config["description"],
        price=config["price"],
        effects=[effect],
        unlock_condition=unlock_condition,
    )


class UnlockManager:
    def __init__(self, engine: CookeyTyper) -> None:
        self.engine = engine

    def check_unlocks(self) -> None:
        self._check_facility_unlocks()
        self._check_upgrade_unlocks()

    def _check_facility_unlocks(self) -> None:
        facility_list = list(self.engine.facilities.values())

        for i, facility in enumerate(facility_list):
            if facility.visual_state == VisualState.HIDDEN:
                if i < 2:
                    facility.visual_state = VisualState.COVERED
                elif facility_list[i - 2].visual_state == VisualState.SHOWN:
                    facility.visual_state = VisualState.COVERED

            if facility.visual_state == VisualState.COVERED:
                total = self.engine.stats.total_cookies_ascension
                if total >= facility.base_cost:
                    facility.visual_state = VisualState.SHOWN

    def _check_upgrade_unlocks(self) -> None:
        for upgrade in self.engine.upgrades.values():
            if upgrade.is_purchased:
                continue
            if upgrade in self.engine.available_upgrades:
                continue
            if upgrade.unlock_condition(self.engine):
                self.engine.available_upgrades.append(upgrade)


class UpgradeManager:
    def __init__(self, engine: CookeyTyper) -> None:
        self.engine = engine

    def purchase_upgrade(self, upgrade_type: UpgradeTypes) -> bool:
        upgrade = self.engine.upgrades.get(upgrade_type)
        if upgrade is None:
            print(f"Upgrade {upgrade_type} not found.")
            return False

        if upgrade.is_purchased:
            print(f"Upgrade '{upgrade.name}' is already purchased.")
            return False

        if upgrade not in self.engine.available_upgrades:
            print(f"Upgrade '{upgrade.name}' is not yet available.")
            return False

        if self.engine.cookies < upgrade.price:
            print(
                f"Not enough cookies. Need {upgrade.price}, have {int(self.engine.cookies)}."
            )
            return False

        self.engine.delta_cookie(-upgrade.price, CookieSource.UPGRADE_PURCHASE)
        upgrade.is_purchased = True
        self.engine.available_upgrades.remove(upgrade)
        self._apply_effects(upgrade)
        print(f"Purchased upgrade: {upgrade.name}")
        return True

    def _apply_effects(self, upgrade: Upgrade) -> None:
        for effect in upgrade.effects:
            target = effect.target
            if isinstance(target, FacilityTypes):
                facility = self.engine.facilities.get(target)
                if facility:
                    modifier = Modifier(
                        source_type=ModifierSourceType.UPGRADE,
                        source_id=upgrade.type,
                        effect_type=effect.effect_type,
                        value=effect.value,
                    )
                    facility.add_modifier(modifier)
            elif target == "Global":
                if effect.effect_type == EffectType.MULTIPLIER:
                    self.engine.global_multipliers["global"] *= effect.value
                elif effect.effect_type == EffectType.ADD:
                    self.engine.global_multipliers["cps"] += effect.value
            elif target == "Click":
                if effect.effect_type == EffectType.MULTIPLIER:
                    self.engine.global_multipliers["cpt"] *= effect.value
                elif effect.effect_type == EffectType.ADD:
                    pass
