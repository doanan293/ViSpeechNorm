"""Single letters, e.g. "chữ A" or "H 5 N 1", read by their Vietnamese names."""

import re

from speech_text_normalizer.symbols import WORD_CHARS

_LETTER_NAMES = {
    "a": "a", "b": "bê", "c": "xê", "d": "dê", "đ": "đê", "f": "ép", "g": "gờ", "h": "hát",
    "i": "i", "j": "gi", "k": "ka", "l": "lờ", "m": "mờ", "n": "en nờ", "o": "o", "p": "pê",
    "q": "quy", "r": "rờ", "s": "ét", "t": "ti", "v": "vi", "w": "vê kép", "x": "ích", "z": "dét",
}  # fmt: skip
_LETTER = re.compile(
    r"(chữ|chữ cái|kí tự|ký tự)?(\s)(\"|\')?(" + "|".join(_LETTER_NAMES) + r")(.)?",
    re.IGNORECASE,
)


def _expand(match: re.Match[str]) -> str:
    leading, _space, quote, char, trailing = match.groups(default="")
    if trailing in WORD_CHARS:  # an empty trailing match also keeps the text unchanged
        return match.group(0)
    trailing = "" if trailing == "." else trailing
    return f"{leading} {quote}{_LETTER_NAMES[char.lower()]}{trailing} "


def normalize(text: str) -> str:
    return _LETTER.sub(_expand, text)
