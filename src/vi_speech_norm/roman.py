"""Roman numerals up to 39, e.g. "thế kỷ XX" -> "thế kỷ hai mươi"."""

import re

from vi_speech_norm.symbols import NOT_WORD
from vi_speech_norm.vi_number import number_to_words

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
_MAX_READ = 39
_ROMAN = re.compile(
    r"(\b(?!LLC)(?=[MDCLXVI]+\b)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\b)"
)
_LETTER_NAME = re.compile(r"(chữ|chữ cái|kí tự|ký tự)(\s)(\"|\')?([A-Z]+)(\"|\')?" + NOT_WORD)


def roman_to_int(numeral: str) -> int:
    """Subtractive notation: a smaller value before a larger one is subtracted."""
    # Algorithm from https://stackoverflow.com/questions/19308177 (CC BY-SA), see NOTICE.
    total = 0
    for index, char in enumerate(numeral):
        value = _VALUES[char]
        following = _VALUES[numeral[index + 1]] if index + 1 < len(numeral) else 0
        total += value if value >= following else -value
    return total


def _expand(match: re.Match[str]) -> str:
    numeral = match.group(0).strip()
    value = roman_to_int(numeral)
    if value > _MAX_READ:
        return numeral
    return f" {number_to_words(str(value))} "


def normalize(text: str) -> str:
    text = _LETTER_NAME.sub(lambda m: m.group(0).lower(), text)
    return _ROMAN.sub(_expand, text)
