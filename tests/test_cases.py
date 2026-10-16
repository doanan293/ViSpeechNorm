"""Every input/expected pair from the original unittest suite, grouped by normalization step."""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from speech_text_normalizer import normalize
from speech_text_normalizer.abbreviations import (
    normalize_abbreviations_vi,
    normalize_speacial_symbol_vi,
)
from speech_text_normalizer.acronyms import spell_acronyms_vi
from speech_text_normalizer.currency import normalize_currency_vi
from speech_text_normalizer.datetime_vi import normalize_date, normalize_time
from speech_text_normalizer.letters import normalize_letter_vi
from speech_text_normalizer.measurements import normalize_measurement_vi
from speech_text_normalizer.numbers import normalize_number_vi
from speech_text_normalizer.roman import normalize_roman_numbers
from speech_text_normalizer.whitespace import collapse_whitespace, pad

STEP_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "symbols": normalize_speacial_symbol_vi,
    "abbreviations": normalize_abbreviations_vi,
    "acronyms": spell_acronyms_vi,
    "currency": normalize_currency_vi,
    "datetime": normalize_date,
    "time": normalize_time,
    "letters": normalize_letter_vi,
    "measurements": normalize_measurement_vi,
    "numbers": normalize_number_vi,
    "roman": normalize_roman_numbers,
    "pipeline": normalize,
}
KNOWN_FAILURES = {
    ("letters", "H 5 N 1"),
    ("numbers", "-1"),
    ("numbers", "-1.000"),
    ("numbers", "1,23"),
    ("numbers", "1,002"),
    ("numbers", "0,02"),
    ("numbers", "-2,7"),
}
CASES = [
    pytest.param(
        step,
        case["input"],
        case["expected"],
        id=f"{step}:{case['input']}",
        marks=[pytest.mark.xfail(strict=True)] if (step, case["input"]) in KNOWN_FAILURES else [],
    )
    for step, items in json.loads((Path(__file__).parent / "cases.json").read_text()).items()
    for case in items
]


@pytest.mark.parametrize(("step", "text", "expected"), CASES)
def test_step(step: str, text: str, expected: str) -> None:
    result = STEP_FUNCTIONS[step](pad(text))
    assert collapse_whitespace(result) == expected
