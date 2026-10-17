"""Every input/expected pair from the original unittest suite, grouped by normalization step."""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from vi_speech_norm import (
    abbreviations,
    acronyms,
    currency,
    datetime_vi,
    letters,
    measurements,
    normalize,
    numbers,
    roman,
)
from vi_speech_norm.whitespace import collapse_whitespace, pad

STEP_FUNCTIONS: dict[str, Callable[[str], str]] = {
    "symbols": abbreviations.expand_special_symbols,
    "abbreviations": abbreviations.normalize,
    "acronyms": acronyms.normalize,
    "currency": currency.normalize,
    "datetime": datetime_vi.normalize_date,
    "time": datetime_vi.normalize_time,
    "letters": letters.normalize,
    "measurements": measurements.normalize,
    "numbers": numbers.normalize,
    "roman": roman.normalize,
    "pipeline": normalize,
}
KNOWN_FAILURES: set[tuple[str, str]] = set()
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
