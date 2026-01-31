from __future__ import annotations

SUFFIXES = [
    "",
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
    "undecillion",
    "duodecillion",
    "tredecillion",
    "quattuordecillion",
    "quindecillion",
    "sexdecillion",
    "septendecillion",
    "octodecillion",
    "novemdecillion",
    "vigintillion",
]


def format_cookies(value: float | int, show_unit: bool = True) -> str:
    if value < 0:
        return f"-{format_cookies(-value, show_unit)}"

    int_value = int(value)

    if int_value < 1000:
        result = str(int_value)
    else:
        suffix_index = 0
        scaled = float(int_value)

        while scaled >= 1000 and suffix_index < len(SUFFIXES) - 1:
            scaled /= 1000
            suffix_index += 1

        result = f"{scaled:.3f} {SUFFIXES[suffix_index]}"

    if show_unit:
        cookie_word = "cookie" if int_value == 1 else "cookies"
        return f"{result} {cookie_word}"
    return result


def format_cps(value: float) -> str:
    if value < 0:
        return f"-{format_cps(-value)}"

    if value < 1000:
        if value == int(value):
            return f"{int(value)} cps"
        return f"{value:.1f} cps"

    suffix_index = 0
    scaled = value

    while scaled >= 1000 and suffix_index < len(SUFFIXES) - 1:
        scaled /= 1000
        suffix_index += 1

    return f"{scaled:.3f} {SUFFIXES[suffix_index]} cps"
