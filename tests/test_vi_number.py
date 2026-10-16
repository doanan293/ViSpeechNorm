import json
from pathlib import Path

import pytest

from speech_text_normalizer.vi_number import digits_to_words, number_to_words

GOLDEN = json.loads((Path(__file__).parent / "golden" / "numbers.json").read_text())
INTEGERS = sorted((k, v) for k, v in GOLDEN["n2w"].items() if k != "0")


@pytest.mark.parametrize(("number", "expected"), INTEGERS, ids=[k for k, _ in INTEGERS])
def test_number_to_words_matches_reference_readings(number: str, expected: str) -> None:
    assert number_to_words(number) == expected


def test_zero_reads_khong() -> None:
    assert number_to_words("0") == "không"
    assert number_to_words("00") == "không"


def test_leading_zeros_are_ignored() -> None:
    assert number_to_words("03") == "ba"


@pytest.mark.parametrize(("digits", "expected"), sorted(GOLDEN["n2w_single"].items()))
def test_digits_to_words(digits: str, expected: str) -> None:
    assert digits_to_words(digits) == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [("1.000", "một nghìn"), ("2 000 000 000", "hai tỷ"), ("9.999", "chín nghìn chín trăm chín mươi chín")],
)
def test_thousand_separators_are_ignored(number: str, expected: str) -> None:
    assert number_to_words(number) == expected


def test_vietnam_country_code_reads_as_leading_zero() -> None:
    assert digits_to_words("+84987") == "không chín tám bảy"
