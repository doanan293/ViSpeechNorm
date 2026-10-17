"""Dates, date ranges, quarters and clock times."""

import re

from vi_speech_norm.roman import normalize as normalize_roman
from vi_speech_norm.symbols import NOT_WORD, NOT_WORD_FOR_DATE
from vi_speech_norm.vi_number import number_to_words

DAYS_IN_MONTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
ROMAN_QUARTERS = ("I", "II", "III", "IV")
_SEPARATOR = r"(\/|-|\.)"
_DAY_PERIODS = r"(ngày|hôm|sáng|trưa|chiều|tối|đêm|khuya)"
_QUARTER = r"(\d{1,2}|(I|II|III|IV))"
_FLAGS = re.IGNORECASE

_QUARTER_YEAR = re.compile(
    r"(quý)" + NOT_WORD + _QUARTER + _SEPARATOR + r"(\d{4})" + NOT_WORD_FOR_DATE, _FLAGS
)
_FULL_DATE = re.compile(
    r"(ngày)?" + NOT_WORD + r"(\d{1,2})" + _SEPARATOR + r"(\d{1,2})" + _SEPARATOR + r"(\d{4})"
    + NOT_WORD_FOR_DATE,
    _FLAGS,
)  # fmt: skip
_FULL_DATE_RANGE = re.compile(
    r"(ngày)?" + NOT_WORD + r"(\d{1,2})(\-)(\d{1,2})" + _SEPARATOR + r"(\d{1,2})" + _SEPARATOR
    + r"(\d{4})" + NOT_WORD_FOR_DATE,
    _FLAGS,
)  # fmt: skip
_DAY_MONTH = re.compile(
    _DAY_PERIODS + NOT_WORD + r"(\d{1,2})" + _SEPARATOR + r"(\d{1,2})" + NOT_WORD_FOR_DATE, _FLAGS
)
_DAY_MONTH_RANGE = re.compile(
    r"(ngày)?" + NOT_WORD + r"(\d{1,2})(\-)(\d{1,2})" + _SEPARATOR + r"(\d{1,2})"
    + NOT_WORD_FOR_DATE,
    _FLAGS,
)  # fmt: skip
_MONTH_YEAR = re.compile(
    r"(tháng)?" + NOT_WORD + r"(\d{1,2})" + _SEPARATOR + r"(\d{4})" + NOT_WORD_FOR_DATE, _FLAGS
)
_MONTH_YEAR_RANGE = re.compile(
    r"(tháng)?" + NOT_WORD + r"(\d{1,2})(\-)(\d{1,2})" + _SEPARATOR + r"(\d{4})"
    + NOT_WORD_FOR_DATE,
    _FLAGS,
)  # fmt: skip
_FULL_TIME = re.compile(
    NOT_WORD + r"(\d{1,2})(g|:|h)(\d{1,2})(p|:|m)(\d{1,2})(s|g)?" + NOT_WORD_FOR_DATE, _FLAGS
)
_TIME = re.compile(NOT_WORD + r"(\d{1,2})(g|:|h)(\d{1,2})(p|m)?" + NOT_WORD_FOR_DATE, _FLAGS)


def remove_leading_zeros(text: str) -> str:
    """'05' -> '5' and '00' -> '0', but a decimal like '0,5' keeps its zero."""
    text = text.strip()
    while len(text) > 1 and text[0] == "0" and text[1] != ",":
        text = text[1:]
    return text or "0"


def _read(number: str) -> str:
    return number_to_words(remove_leading_zeros(number))


def _is_valid_date(day: int, month: int) -> bool:
    return 1 <= month <= len(DAYS_IN_MONTH) and 1 <= day <= DAYS_IN_MONTH[month - 1]


def _is_valid_time(hour: int, minute: int, second: int = 0) -> bool:
    return 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60  # noqa: PLR2004


def _full_date(match: re.Match[str]) -> str:
    prefix, space, day, separator, month, _sep, year, suffix = match.groups(default="")
    if not _is_valid_date(int(day), int(month)) or prefix == separator:
        return match.group(0)
    return f"{space} ngày {_read(day)} tháng {_read(month)} năm {_read(year)}{suffix} "


def _full_date_range(match: re.Match[str]) -> str:
    _prefix, space, start, _dash, end, _sep, month, _sep2, year, suffix = match.groups(default="")
    if not (_is_valid_date(int(start), int(month)) and _is_valid_date(int(end), int(month))):
        return match.group(0)
    return (
        f"{space} ngày {_read(start)} đến ngày {_read(end)} tháng {_read(month)} "
        f"năm {_read(year)}{suffix} "
    )


def _day_month(match: re.Match[str]) -> str:
    prefix, space, day, separator, month, suffix = match.groups(default="")
    prefix = prefix if prefix.lower() == "ngày" else f"{prefix} ngày"
    if not _is_valid_date(int(day), int(month)) or space == separator:
        return match.group(0)
    return f"{space}{prefix}{space}{_read(day)} tháng {_read(month)}{suffix} "


def _day_month_range(match: re.Match[str]) -> str:
    _prefix, space, start, _dash, end, _sep, month, suffix = match.groups(default="")
    if not (_is_valid_date(int(start), int(month)) and _is_valid_date(int(end), int(month))):
        return match.group(0)
    return f"{space} ngày {_read(start)} đến ngày {_read(end)} tháng {_read(month)}{suffix} "


def _month_year(match: re.Match[str]) -> str:
    _prefix, space, month, separator, year, suffix = match.groups(default="")
    if not _is_valid_date(1, int(month)) or space == separator:
        return match.group(0)
    return f"{space} tháng {_read(month)} năm {_read(year)}{suffix} "


def _month_year_range(match: re.Match[str]) -> str:
    _prefix, space, start, dash, end, separator, year, suffix = match.groups(default="")
    valid = _is_valid_date(1, int(start)) and _is_valid_date(1, int(end))
    if not valid or dash == separator:
        return match.group(0)
    return f"{space} tháng {_read(start)} đến tháng {_read(end)} năm {_read(year)}{suffix} "


def _quarter_year(match: re.Match[str]) -> str:
    _word, space, quarter, _roman, separator, year, suffix = match.groups(default="")
    if quarter in ROMAN_QUARTERS:
        spoken = normalize_roman(quarter)
    else:
        if not 1 <= int(quarter) <= len(ROMAN_QUARTERS) or space == separator:
            return match.group(0)
        spoken = _read(quarter)
    return f"{space} quý {spoken} năm {_read(year)}{suffix} "


def _time(match: re.Match[str]) -> str:
    prefix, hour, _sep, minute, _unit, ending = match.groups(default="")
    if not _is_valid_time(int(hour), int(minute)):
        return match.group(0)
    return f"{prefix} {_read(hour)} giờ {_read(minute)} phút{ending} "


def _full_time(match: re.Match[str]) -> str:
    prefix, hour, _sep, minute, _sep2, second, _unit, ending = match.groups(default="")
    if not _is_valid_time(int(hour), int(minute), int(second)):
        return match.group(0)
    return f"{prefix} {_read(hour)} giờ {_read(minute)} phút {_read(second)} giây{ending} "


_DATE_RULES = (
    (_QUARTER_YEAR, _quarter_year),
    (_MONTH_YEAR_RANGE, _month_year_range),
    (_FULL_DATE_RANGE, _full_date_range),
    (_FULL_DATE, _full_date),
    (_MONTH_YEAR, _month_year),
    (_DAY_MONTH_RANGE, _day_month_range),
    (_DAY_MONTH, _day_month),
)


def normalize_date(text: str) -> str:
    for pattern, expand in _DATE_RULES:
        text = pattern.sub(expand, text)
    return text


def normalize_time(text: str) -> str:
    return _TIME.sub(_time, _FULL_TIME.sub(_full_time, text))


def normalize(text: str) -> str:
    return normalize_time(normalize_date(text))
