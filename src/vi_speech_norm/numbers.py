"""Numbers: integers, decimals, negatives, ranges, ordinals, products and phone numbers."""

import re

from vi_speech_norm.datetime_vi import remove_leading_zeros
from vi_speech_norm.symbols import NOT_LETTER, WORD_CHARS
from vi_speech_norm.vi_number import digits_to_words, number_to_words

_PLAIN = r"\d+"
_DECIMAL = r"\d+,\d+"
_DOT_GROUPS = (r"\d+\.\d{3}\.\d{3}\.\d{3}", r"\d+\.\d{3}\.\d{3}", r"\d+\.\d{3}")
_SPACE_GROUPS = (r"\d+\s\d{3}\s\d{3}\s\d{3}", r"\d+\s\d{3}\s\d{3}", r"\d+\s\d{3}")
_ANY_NUMBER = "(" + "|".join((_DECIMAL, *_DOT_GROUPS, *_SPACE_GROUPS, _PLAIN)) + ")"
_RANGE_PREFIX = r"(từ|tới|còn|đến|khoảng|sau)"

_NUMBER = re.compile(r"(.)(-)?" + _ANY_NUMBER)
_RANGE = re.compile(
    _RANGE_PREFIX + r"(.)(-)?" + _ANY_NUMBER + r"(-|\s\-\s)(-)?" + _ANY_NUMBER + NOT_LETTER,
    re.IGNORECASE,
)
_PRODUCT = re.compile("(" + _PLAIN + r")(x|\sx\s)(" + _PLAIN + ")")
_PHONE = re.compile(r"(((\+84|84|0|0084))(3|5|7|8|9))+([0-9]{8})")
_ORDINAL = re.compile(r"(thứ|hạng)(\s)(1|4)")
_SPECIAL_ORDINALS = {"1": "nhất", "4": "tư"}


def read_number(number: str, *, negative: bool = False) -> str:
    """Read an integer or a decimal with a comma ("2,07" -> "hai phẩy không bảy")."""
    whole, _, fraction = number.partition(",")
    words = number_to_words(whole)
    if fraction:
        zeros = len(fraction) - len(fraction.lstrip("0"))
        rest = fraction[zeros:]
        words += " phẩy " + " ".join(["không"] * zeros + ([number_to_words(rest)] if rest else []))
    return ("âm " if negative else "") + words


def _number(match: re.Match[str]) -> str:
    prefix, minus, number = match.groups(default="")
    number = remove_leading_zeros(number)
    if prefix in WORD_CHARS:
        # "-" right after a word is a hyphen, not a minus sign
        return f"{prefix} {minus}{read_number(number)} "
    return f"{prefix} {read_number(number, negative=minus == '-')} "


def _phone(match: re.Match[str]) -> str:
    return digits_to_words(match.group(0).strip())


def _range(match: re.Match[str]) -> str:
    word, prefix, minus_start, start, _dash, minus_end, end, ending = match.groups(default="")
    if prefix in WORD_CHARS:
        return match.group(0)
    first = read_number(start, negative=minus_start == "-")
    last = read_number(end, negative=minus_end == "-")
    return f"{word}{prefix}{first} đến {last}{ending}"


def _ordinal(match: re.Match[str]) -> str:
    word, space, number = match.groups()
    return word + space + _SPECIAL_ORDINALS.get(number, number_to_words(number))


def _product(match: re.Match[str]) -> str:
    return f"{number_to_words(match.group(1))} nhân {number_to_words(match.group(3))}"


def normalize(text: str) -> str:
    text = _ORDINAL.sub(_ordinal, text)
    text = _PRODUCT.sub(_product, text)
    text = _RANGE.sub(_range, text)
    text = _PHONE.sub(_phone, text)
    return _NUMBER.sub(_number, text)
