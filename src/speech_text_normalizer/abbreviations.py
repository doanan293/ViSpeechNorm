"""Common abbreviations, special symbols and web addresses."""

import re

from speech_text_normalizer._data import table

_ABBREVIATIONS = {
    key.lower(): value for key, value in table("abbreviations.toml", "abbreviations").items()
}
_ABBREVIATION = re.compile(
    r"\b(" + "|".join(re.escape(key) for key in _ABBREVIATIONS) + r")\b", re.IGNORECASE
)
_PERCENT = re.compile(r"[ ]?%")
_URL = re.compile(r"([a-zA-Z])\.(com|gov|org|vn|com.vn|edu.vn)")
_SYMBOLS = (
    (re.compile("&"), " và "),
    (re.compile("@"), " a còng "),
    (re.compile(r"\+"), " cộng "),
    (re.compile("//"), " xuyệt "),
)


def expand_special_symbols(text: str) -> str:
    text = _PERCENT.sub(" phần trăm", text)
    for pattern, spoken in _SYMBOLS:
        text = pattern.sub(spoken, text)
    return text


def normalize(text: str) -> str:
    text = expand_special_symbols(text)
    text = _URL.sub(r"\1 chấm \2", text)
    return _ABBREVIATION.sub(lambda m: _ABBREVIATIONS[m.group(0).lower()], text)
