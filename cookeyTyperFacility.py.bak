from math import ceil

from cookeyTyperData import facilities, parameters
from cookeyTyperTypes import FacilityTypes, VisualState
from result import Err, Ok, Result, is_ok


class Facility:
    def __init__(
        self,
        name: str,
        description: str,
        base_cost: int,
        base_cps: int | float,
        init_visual: VisualState,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.base_cost: int = base_cost
        self.base_cps: int | float = base_cps
        self.visual_state: VisualState = init_visual
        self.amount: int = 0
        self.multiplier: float = 1.0
        self.discount: float = 0.0

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
        # if try selling more than you have
        if base_amount + diff_amount < 0:
            diff_amount = -base_amount
            result = False

        # S = C * (r^(n+Δ) - r^n) / (r - 1)
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

    def cps(self) -> float:
        return self.base_cps * self.multiplier * self.amount

    def delta_amount(self, amount: int = 1) -> bool:
        if amount < 0:
            if self.amount < amount:
                print(f"You only have {self.amount} {self.name}(s)")
                return False
        self.amount += amount
        return True


def get_facilities() -> dict[FacilityTypes, Facility]:
    facilities_dict: dict[FacilityTypes, Facility] = {}
    for facility, config in facilities().items():
        facilities_dict[facility] = Facility(**config)
    return facilities_dict


def into_facility(arg: str) -> Result[FacilityTypes, str]:
    for facility, config in facilities().items():
        if config["name"] == arg.capitalize():
            return Ok(facility)
    else:
        return Err("Invalid Facility Name")
