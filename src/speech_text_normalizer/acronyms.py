"""Acronyms: Vietnamese ones are read as words, listed English ones are spelled out."""

import re

from speech_text_normalizer._data import table, word_list

_SPOKEN = [
    (re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE), value)
    for key, value in table("acronyms.toml", "spoken").items()
]
_SPELLED = frozenset(word_list("acronyms.toml", "spelled", "acronyms"))
_UPPERCASE_WORD = re.compile(r"([a-z]*[A-Z][A-Z]+)s?\.?")


def _spell(match: re.Match[str]) -> str:
    if match.group(1) in _SPELLED:
        return "  ".join(match.group(0))
    return match.group(1)


def normalize(text: str) -> str:
    for pattern, spoken in _SPOKEN:
        text = pattern.sub(spoken, text)
    return _UPPERCASE_WORD.sub(_spell, text)
