import threading
import time

from cookeyTyperData import parameters
from cookeyTyperFacility import Facility, get_facilities
from cookeyTyperHandler import Handler
from cookeyTyperStats import CookeyTyperStats
from cookeyTyperTypes import CookieSource, FacilityTypes


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
        self.handler: Handler = Handler(self)

    def delta_cookie(self, amount: float, source: CookieSource) -> bool:
        with self.lock:
            if self.cookies + amount >= 0:
                self.cookies += amount
                self.stats.on_cookie_amount_change(amount, source)
                return True
            else:
                return False

    def update_cps(self) -> float:
        sum: float = 0.0
        for facility in self.facilities.values():
            sum += facility.cps()
        calibrated_cps: float = (
            sum * self.global_multipliers["global"] * self.global_multipliers["cps"]
        )
        self.cps = calibrated_cps
        return self.cps

    def run(self) -> None:
        self.handler.start()
        while True:
            self.handler.update()
            self.stats.update()
            self.update_cps()

            self.delta_cookie(
                self.cps / parameters()["tick_rate"], CookieSource.FACILITY
            )
            sleep = 1 / parameters()["tick_rate"]
            time.sleep(sleep)
