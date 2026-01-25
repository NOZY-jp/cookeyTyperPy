from __future__ import annotations

import difflib
import queue
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cookeyTyperCore import CookeyTyper

from cookeyTyperData import random_sentence
from cookeyTyperFacility import into_facility
from cookeyTyperTypes import (Command, CommandFacility, CommandHelp,
                              CommandInspectCookieCount,
                              CommandInspectCookiePerSecond,
                              CommandInspectCookiePerType, CommandUserInput,
                              CookieSource, Operations, VisualState)
from result import Err, Ok, Result, is_err


def spawn_handler_thread(q: queue.Queue[str]) -> None:
    while True:
        q.put(input())


class Handler:
    def __init__(self, engine: CookeyTyper) -> None:
        self.engine: CookeyTyper = engine
        self.queue: queue.Queue[str] = queue.Queue()
        self.handler_thread: threading.Thread | None = None
        self.target: str = "Hello Cookey Typer!"

    def start(self) -> None:
        if self.handler_thread is not None:
            return

        self.handler_thread = threading.Thread(
            target=spawn_handler_thread, args=(self.queue,), daemon=True
        )
        self.handler_thread.start()
        print("=" * 70)
        print("Target:")
        print(self.target)

    def update(self) -> bool:
        try:
            raw_input = self.queue.get_nowait()
            command = self.parse_command(raw_input)
            match command:
                case Ok(val):
                    self.execute_command(val)
                    self.target = random_sentence()
                    print("=" * 70)
                    print("Target:")
                    print(self.target)

                    return True
                case Err(str):
                    print(str)
                    print("=" * 70)
                    print("Target:")
                    print(self.target)
                    self.engine.delta_cookie(1, CookieSource.TYPING)
                    return False
        except queue.Empty:
            return False

    def calculate_typing_score(self, target: str, user_input: str) -> tuple[int, int]:
        matcher = difflib.SequenceMatcher(None, target, user_input)
        correct_chars = sum(match.size for match in matcher.get_matching_blocks())
        accuracy_score = 2 * correct_chars - len(user_input)
        return (correct_chars, max(0, accuracy_score))

    def parse_operation(self, arg: str) -> Result[Operations, str]:
        match arg.lower():
            case "buy" | "b":
                return Ok(Operations.BUY)
            case "sell" | "s":
                return Ok(Operations.SELL)
            case "detail" | "d":
                return Ok(Operations.DETAIL)
            case "ls":
                return Ok(Operations.LS)
            case "la":
                return Ok(Operations.LA)
            case _:
                return Err("Invalid Operation Argument")

    def parse_command(self, raw_input: str) -> Result[Command, str]:
        args: list[str] = raw_input.lower().split()
        match args:
            case ["facility" | "fac" | "f", op_str, target_str, amount_str]:
                op = self.parse_operation(op_str)
                if is_err(op):
                    return Err(op.error)

                target = into_facility(target_str)
                if is_err(target):
                    return Err(target.error)

                try:
                    amount = int(amount_str)
                except ValueError:
                    return Err("Invalid Purchase Amount")

                return Ok(
                    CommandFacility(
                        operation=op.value,
                        target=target.value,
                        amount=amount,
                    )
                )

            case ["facility" | "fac" | "f", op_str, target_str]:
                op = self.parse_operation(op_str)
                if is_err(op):
                    return Err(op.error)

                target = into_facility(target_str)
                if is_err(target):
                    return Err(target.error)

                # amount default = 1
                return Ok(CommandFacility(operation=op.value, target=target.value))

            case ["facility" | "fac" | "f", op_str]:
                op = self.parse_operation(op_str)
                if is_err(op):
                    return Err(op.error)

                return Ok(CommandFacility(operation=op.value))

            case ["facility" | "fac" | "f"]:
                return Ok(CommandFacility(operation=Operations.LS))

            # case ["upgrade" | "upg" | "u", op_str, target_str]:
            #     op = self.parse_operation(op_str)
            #     if is_err(op):
            #         return Err(op.error)
            #
            #     target = into_upgrade(target_str)
            #     if is_err(target):
            #         return Err(target.error)
            #
            #     return Ok(CommandUpgrade(operation=op.value, target=target.value))
            #
            # case ["upgrade" | "upg" | "u", op_str]:
            #     op = self.parse_operation(op_str)
            #     if is_err(op):
            #         return Err(op.error)
            #
            #     return Err("Usage: [upgrade/upg/u] [buy/detail/ls/la] [upgrade_id]")
            #
            # case ["upgrade" | "upg" | "u"]:
            #     return Ok(CommandUpgrade(operation=Operations.LS))

            case ["help" | "h" | "?"]:
                return Ok(CommandHelp())

            case ["cc"]:
                return Ok(CommandInspectCookieCount())

            case ["cps"]:
                return Ok(CommandInspectCookiePerSecond())

            case ["cpt"]:
                return Ok(CommandInspectCookiePerType())

            case _:
                return Ok(CommandUserInput(content=raw_input))

    def execute_command(self, command: Command) -> bool:
        match command:
            case CommandHelp():
                print("""
================ CookeyTyper Help ================
[Usage]
  <command> <operation> [target] [amount]

[Commands]
  facility (f, fac) : Manage facilities
    <operations>
      ls         : List owned facilities
      la         : List all available facilities
      buy (b)    : Buy facilities
                   Ex: 'f buy cursor 10'
      sell (s)   : Sell facilities (50% return)
      detail (d) : Show detailed stats of a facility

  help (h, ?)       : Show this help message

[Inspectors]
  cc   : Show current Cookie Count
  cps  : Show current Cookies Per Second
  cpt  : Show Cookies Per Type (production breakdown)
==================================================
""")

            case CommandFacility():
                match command.operation:
                    case Operations.LS:
                        header = f"| {'Name':<16} | {'Owned':^6} | {'Cost':>15} | {'Description'}"

                        print(f"{'=' * 27} Facility  List {'=' * 27}")
                        print(header)
                        print("-" * 70)

                        for facility in self.engine.facilities.values():
                            cost_str = f"{int(facility.next_cost())}"
                            if facility.visual_state == VisualState.SHOWN:
                                print(
                                    f"| {facility.name:<16} "
                                    f"| {facility.amount:^6} "
                                    f"| {cost_str:>15} "
                                    f"| {facility.description}"
                                )
                            elif facility.visual_state == VisualState.COVERED:
                                print(
                                    f"| {'---':<16} "
                                    f"| {'-':^6} "
                                    f"| {cost_str:>15} "
                                    f"| {'---'}"
                                )

                        print("=" * 70)
                    case Operations.LA:
                        header = f"| {'Name':<16} | {'Owned':^6} | {'Unit CPS':>10} | {'CPS':>10} | {'Cost':>15} | {'Description'}"
                        total_width = 95

                        print(f"{'=' * 39}  Facility List  {'=' * 39}")
                        print(header)
                        print("-" * total_width)

                        for facility in self.engine.facilities.values():
                            cost_str = f"{int(facility.next_cost()):,}"

                            if facility.visual_state == VisualState.SHOWN:
                                unit_cps_str = f"{facility.cps():.1f}"
                                cps_str = f"{facility.cps() * facility.amount:.1f}"
                                print(
                                    f"| {facility.name:<16} "
                                    f"| {facility.amount:^6} "
                                    f"| {unit_cps_str:>10} "
                                    f"| {cps_str:>10} "
                                    f"| {cost_str:>15} "
                                    f"| {facility.description}"
                                )
                            elif facility.visual_state == VisualState.COVERED:
                                print(
                                    f"| {facility.name:<16} "
                                    f"| {'-':^6} "
                                    f"| {'-':>10} "
                                    f"| {'-':>10} "
                                    f"| {cost_str:>15} "
                                    f"| {'???'}"
                                )

                        print("=" * total_width)

                    case Operations.DETAIL:
                        target = command.target
                        if target is None:
                            print("-" * 50)
                            print(
                                "[CRITICAL ERROR] Target is None for DETAIL operation."
                            )
                            print(
                                "This should NOT happen if the parser is working correctly."
                            )
                            print(
                                "Please report this bug to the author with your input."
                            )
                            print("-" * 50)
                            return False
                        facility = self.engine.facilities.get(target)
                        if facility is None:
                            print("-" * 50)
                            print(
                                "[CRITICAL ERROR] Facility is None for DETAIL operation."
                            )
                            print(
                                "This should NOT happen if the parser is working correctly."
                            )
                            print(
                                "Please report this bug to the author with your input."
                            )
                            print("-" * 50)
                            return False

                        if facility.visual_state == VisualState.SHOWN:
                            print(f"\n{'=' * 22} Facility Detail {'=' * 22}")
                            print(f" Name        : {facility.name}")
                            print(f" Description : {facility.description}")
                            print("-" * 61)
                            print(f" Owned       : {facility.amount}")
                            unit_cps = facility.cps()
                            total_cps = unit_cps * facility.amount
                            print(f" Base CPS    : {unit_cps:.1f} / unit")
                            print(f" Total CPS   : {total_cps:,.1f} (Contribution)")
                            print(
                                f" Next Cost   : {int(facility.next_cost()):,} cookies"
                            )
                            print(f"{'=' * 61}\n")
                        elif facility.visual_state == VisualState.COVERED:
                            print(f"\n{'=' * 22} Facility Detail {'=' * 22}")
                            print(" Name        : ???")
                            print(" Description : ???")
                            print("-" * 61)
                            print(" Owned       : -")
                            print(" Base CPS    : 0.0 / unit")
                            print(" Total CPS   : 0.0 (Contribution)")
                            print(
                                f" Next Cost   : {int(facility.next_cost()):,} cookies"
                            )
                            print(f"{'=' * 61}\n")
                        else:
                            print("Invalid Facility Name")
                            return False

                    case Operations.BUY:
                        target = command.target
                        if target is None:
                            print("-" * 50)
                            print("[CRITICAL ERROR] Target is None for BUY operation.")
                            print(
                                "This should NOT happen if the parser is working correctly."
                            )
                            print(
                                "Please report this bug to the author with your input."
                            )
                            print("-" * 50)
                            return False
                        facility = self.engine.facilities.get(target)
                        if facility is None:
                            print("-" * 50)
                            print(
                                "[CRITICAL ERROR] Facility is None for BUY operation."
                            )
                            print(
                                "This should NOT happen if the parser is working correctly."
                            )
                            print(
                                "Please report this bug to the author with your input."
                            )
                            print("-" * 50)
                            return False
                        if facility.visual_state == VisualState.HIDDEN:
                            print("Invalid Facility Name")
                            return False
                        amount = command.amount
                        if amount < 0:
                            print("Expected Positive Integer for perchasing amount.")
                            return False

                        cost = facility.get_cookie_delta(diff_amount=amount)
                        if is_err(cost):
                            print("-" * 50)
                            print(
                                "[CRITICAL ERROR] Cost calculation error for BUY operation."
                            )
                            print(
                                "This should NOT happen if the cost calculator is working correctly."
                            )
                            print(
                                "Please report this bug to the author with your input."
                            )
                            print("-" * 50)
                            return False
                        else:
                            cost = cost.value
                        if self.engine.delta_cookie(
                            cost, CookieSource.FACILITY_PURCHASE
                        ):
                            facility.delta_amount(amount)
                            print(
                                f"Purchased {(str(amount) + ' ') if amount == 1 else ''}{target.name} for {abs(cost)} cookies"
                            )
                        else:
                            print("Not enough cookies!")
                            print(f"Cost: {abs(cost)}")
                            print(f"Current Cookies: {self.engine.cookies}")

                    case _:
                        pass
            case CommandInspectCookieCount():
                print(f"Current Cookie Count: {int(self.engine.cookies)}")
            case CommandInspectCookiePerSecond():
                print(f"Current Cookie Per Second: {self.engine.cps}")
            case CommandInspectCookiePerType():
                print(f"Current Cookie Per Type: {self.engine.cpt}")
            case CommandUserInput():
                accurate_typing, calibrated_score = self.calculate_typing_score(
                    self.target, command.content
                )
                cookies_gain = (
                    calibrated_score
                    * self.engine.cpt
                    * self.engine.global_multipliers["cpt"]
                )
                print(f"You typed {accurate_typing} characters correctly and")
                print(f"earned {int(cookies_gain)} cookies!")
                self.engine.delta_cookie(cookies_gain, CookieSource.TYPING)

            case _:
                pass

        return True
