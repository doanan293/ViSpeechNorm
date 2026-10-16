"""Currency symbols and codes."""

import re

from speech_text_normalizer._data import table
from speech_text_normalizer.symbols import NOT_LETTER

_CURRENCY = {key.lower(): value for key, value in table("abbreviations.toml", "currency").items()}
_PATTERN = re.compile(
    NOT_LETTER + "(" + "|".join(re.escape(key) for key in _CURRENCY) + ")" + NOT_LETTER,
    re.IGNORECASE,
)


def _expand(match: re.Match[str]) -> str:
    prefix, currency, suffix = match.group(1), match.group(2), match.group(3)
    if (currency == "Đ" and suffix == ".") or currency in (prefix, suffix):
        return match.group(0)
    return prefix + _CURRENCY.get(currency.lower(), currency) + suffix


def normalize(text: str) -> str:
    return _PATTERN.sub(_expand, text)
