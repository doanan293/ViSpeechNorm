"""The normalization pipeline: one fixed order of steps."""

import re
import unicodedata
from collections.abc import Callable, Sequence

from vi_speech_norm import (
    abbreviations,
    acronyms,
    currency,
    datetime_vi,
    letters,
    measurements,
    numbers,
    roman,
)
from vi_speech_norm.whitespace import collapse_whitespace, pad

_SLASH = re.compile(r"/")
_INNER_HYPHEN = re.compile(r"([^\s])-([^\s])")
_APRIL = re.compile("tháng bốn", re.IGNORECASE)
_SPACE_AFTER_PUNCTUATION = re.compile(r"([,;:!?])(?=[^\s\d,;:!?.])")


def _unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _symbols(text: str) -> str:
    return _INNER_HYPHEN.sub(r"\1 \2", _SLASH.sub(" trên ", text))


def _months(text: str) -> str:
    return _APRIL.sub("tháng tư", collapse_whitespace(text))


_STEP_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "unicode": _unicode,
    "abbreviations": abbreviations.normalize,
    "roman": roman.normalize,
    "acronyms": acronyms.normalize,
    "datetime": datetime_vi.normalize,
    "measurements": measurements.normalize,
    "currency": currency.normalize,
    "numbers": numbers.normalize,
    "letters": letters.normalize,
    "symbols": _symbols,
    "months": _months,
    "lowercase": str.lower,
}
STEPS: tuple[str, ...] = tuple(_STEP_FUNCTIONS)


def normalize(text: str, *, steps: Sequence[str] | None = None) -> str:
    """Rewrite Vietnamese text into words a TTS engine can read.

    `steps` selects a subset of `STEPS`; they always run in pipeline order.
    """
    chosen = STEPS if steps is None else tuple(steps)
    unknown = [step for step in chosen if step not in _STEP_FUNCTIONS]
    if unknown:
        msg = f"unknown step(s): {', '.join(unknown)}; choose from {', '.join(STEPS)}"
        raise ValueError(msg)
    text = pad(text)
    for step in STEPS:
        if step in chosen:
            text = _STEP_FUNCTIONS[step](text)
    return collapse_whitespace(_SPACE_AFTER_PUNCTUATION.sub(r"\1 ", text))
