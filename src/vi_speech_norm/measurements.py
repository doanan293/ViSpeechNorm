"""Measurement units after numbers, including ratios such as km/h."""

import re

from vi_speech_norm._data import table
from vi_speech_norm.symbols import NOT_LETTER, NOT_WORD

_UNITS = table("units.toml", "units")
_UNIT_ALTERNATION = "(" + "|".join(re.escape(unit) for unit in _UNITS) + ")"
_UNIT = re.compile(NOT_LETTER + _UNIT_ALTERNATION + NOT_WORD)
_RATIO = re.compile(NOT_LETTER + _UNIT_ALTERNATION + "/" + _UNIT_ALTERNATION + NOT_WORD)


def _expand_unit(match: re.Match[str]) -> str:
    prefix, unit, suffix = match.group(1), match.group(2), match.group(3)
    if len(unit) == 1 and not prefix.isdigit():
        return match.group(0)
    return f"{prefix} {_UNITS[unit]} {suffix}"


def _expand_ratio(match: re.Match[str]) -> str:
    prefix, first, second, suffix = match.groups()
    return f"{prefix} {_UNITS[first]} trên {_UNITS[second]}{suffix}"


def normalize(text: str) -> str:
    return _UNIT.sub(_expand_unit, _RATIO.sub(_expand_ratio, text))
