import threading
import time

from cookeyTyperData import parameters, upgrades
from cookeyTyperHandler import Handler
from cookeyTyperModels import Facility, Upgrade, get_facilities
from cookeyTyperStats import CookeyTyperStats
from cookeyTyperSystems import (
    UnlockManager,
    UpgradeManager,
    create_upgrade_from_config,
)
from cookeyTyperTypes import CookieSource, FacilityTypes, UpgradeTypes


class CookeyTyper:
    def __init__(self) -> None:
        self.lock: threading.Lock = threading.Lock()
        self.cookies: float = 0.0
        self.cps: float = 0.0
        self.cpt: float = 1.0
        self.facilities: dict[FacilityTypes, Facility] = get_facilities()
        self.stats: CookeyTyperStats = CookeyTyperStats(self)
        self.global_multipliers: dict[str, float] = {
            "global": 1.0,
            "cpt": 1.0,
            "cps": 1.0,
        }
        self.global_discount: float = 0.0

        self.upgrades: dict[UpgradeTypes, Upgrade] = self._init_upgrades()
        self.available_upgrades: list[Upgrade] = []

        self.unlock_manager: UnlockManager = UnlockManager(self)
        self.upgrade_manager: UpgradeManager = UpgradeManager(self)
        self.handler: Handler = Handler(self)

    def _init_upgrades(self) -> dict[UpgradeTypes, Upgrade]:
        upgrade_dict: dict[UpgradeTypes, Upgrade] = {}
        for upgrade_type in upgrades():
            upgrade_dict[upgrade_type] = create_upgrade_from_config(upgrade_type, self)
        return upgrade_dict

    def delta_cookie(self, amount: float, source: CookieSource) -> bool:
        with self.lock:
            if self.cookies + amount >= 0:
                self.cookies += amount
                self.stats.on_cookie_amount_change(amount, source)
                return True
            else:
                return False

    def update_cps(self) -> float:
        total: float = 0.0
        for facility in self.facilities.values():
            total += facility.cps
        calibrated_cps: float = (
            total * self.global_multipliers["global"] * self.global_multipliers["cps"]
        )
        self.cps = calibrated_cps
        return self.cps

    def run(self) -> None:
        self.handler.start()
        while True:
            self.handler.update()
            self.stats.update()
            self.unlock_manager.check_unlocks()
            self.update_cps()

            self.delta_cookie(
                self.cps / parameters()["tick_rate"], CookieSource.FACILITY
            )
            sleep = 1 / parameters()["tick_rate"]
            time.sleep(sleep)
