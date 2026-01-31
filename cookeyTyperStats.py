from __future__ import annotations

from typing import TYPE_CHECKING

from cookeyTyperData import facilities
from cookeyTyperTypes import CookieSource, FacilityConfig, FacilityTypes, VisualState

if TYPE_CHECKING:
    from cookeyTyperCore import CookeyTyper


class CookeyTyperStats:
    def __init__(self, engine: CookeyTyper) -> None:
        self.engine: CookeyTyper = engine
        self.facility_visual_state_manager: tuple[
            list[FacilityTypes], list[FacilityConfig]
        ] = (list(facilities().keys()), list(facilities().values()))

        self.total_cookies_ever: float = 0
        self.total_cookies_consumed_ever: float = 0
        self.total_cookies_lost_ever: float = 0
        self.total_cookies_ascension: float = 0
        self.total_types: int = 0
        self.total_cookies_by_type: float = 0
        self.total_cookies_by_facilities: float = 0

    def on_cookie_amount_change(
        self, amount: float, source: CookieSource = CookieSource.ELSE
    ) -> None:
        if amount >= 0:
            match source:
                case CookieSource.TYPING:
                    self.total_cookies_by_type += amount
                case CookieSource.FACILITY:
                    self.total_cookies_by_facilities += amount
                case _:
                    pass

            self.total_cookies_ever += amount
            self.total_cookies_ascension += amount
        else:
            match source:
                case CookieSource.FACILITY_PURCHASE | CookieSource.UPGRADE_PURCHASE:
                    self.total_cookies_consumed_ever += abs(amount)
                case _:
                    pass

    def update(self) -> None:
        if (
            self.total_cookies_ascension
            >= self.facility_visual_state_manager[1][0]["base_cost"]
        ):
            if len(self.facility_visual_state_manager[1]) >= 3:
                self.engine.facilities[
                    self.facility_visual_state_manager[0][0]
                ].visual_state = VisualState.SHOWN
                self.engine.facilities[
                    self.facility_visual_state_manager[0][2]
                ].visual_state = VisualState.COVERED

                self.facility_visual_state_manager[0].pop(0)
                self.facility_visual_state_manager[1].pop(0)
