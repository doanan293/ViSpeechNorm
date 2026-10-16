"""The normalization pipeline: one fixed order of steps."""

import re
import unicodedata
from collections.abc import Callable, Sequence

from speech_text_normalizer.abbreviations import normalize_abbreviations_vi
from speech_text_normalizer.acronyms import spell_acronyms_vi
from speech_text_normalizer.currency import normalize_currency_vi
from speech_text_normalizer.datetime_vi import normalize_date, normalize_time
from speech_text_normalizer.letters import normalize_letter_vi
from speech_text_normalizer.measurements import normalize_measurement_vi
from speech_text_normalizer.numbers import normalize_number_vi
from speech_text_normalizer.roman import normalize_roman_numbers
from speech_text_normalizer.whitespace import collapse_whitespace, pad

_SLASH = re.compile(r"/")
_INNER_HYPHEN = re.compile(r"([^\s])-([^\s])")
_APRIL = re.compile("tháng bốn", re.IGNORECASE)
_SPACE_AFTER_PUNCTUATION = re.compile(r"([,;:!?])(?=[^\s\d,;:!?.])")


def _unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _datetime(text: str) -> str:
    return normalize_time(normalize_date(text))


def _symbols(text: str) -> str:
    return _INNER_HYPHEN.sub(r"\1 \2", _SLASH.sub(" trên ", text))


def _months(text: str) -> str:
    return _APRIL.sub("tháng tư", collapse_whitespace(text))


_STEP_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "unicode": _unicode,
    "abbreviations": normalize_abbreviations_vi,
    "roman": normalize_roman_numbers,
    "acronyms": spell_acronyms_vi,
    "datetime": _datetime,
    "measurements": normalize_measurement_vi,
    "currency": normalize_currency_vi,
    "numbers": normalize_number_vi,
    "letters": normalize_letter_vi,
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
