"""Read Vietnamese numbers aloud: whole numbers by place value, or digit by digit."""

DIGITS = ("không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín")
SCALES = ("", "nghìn", "triệu")
_GROUP = 3
_ONE = 1
_FIVE = 5
_BILLION_DIGITS = 9
COUNTRY_CODE = "+84"


def _tens_and_units(tens: int, units: int, *, after_hundreds: bool) -> list[str]:
    words: list[str] = []
    if tens == 0:
        if units:
            if after_hundreds:
                words.append("lẻ")
            words.append(DIGITS[units])
        return words
    words.extend(["mười"] if tens == _ONE else [DIGITS[tens], "mươi"])
    if units == _ONE and tens > _ONE:
        words.append("mốt")
    elif units == _FIVE:
        words.append("lăm")
    elif units:
        words.append(DIGITS[units])
    return words


def _group_words(value: int, *, leading: bool) -> list[str]:
    hundreds, rest = divmod(value, 100)
    tens, units = divmod(rest, 10)
    words: list[str] = []
    if hundreds or not leading:
        words.extend([DIGITS[hundreds], "trăm"])
    words.extend(_tens_and_units(tens, units, after_hundreds=bool(words)))
    return words


def _below_billion(digits: str, *, leading: bool) -> list[str]:
    groups = [int(digits[max(0, end - _GROUP) : end]) for end in range(len(digits), 0, -_GROUP)]
    words: list[str] = []
    for index in range(len(groups) - 1, -1, -1):
        value = groups[index]
        if value == 0:
            continue
        words.extend(_group_words(value, leading=leading and not words and index == len(groups) - 1))
        if SCALES[index]:
            words.append(SCALES[index])
    return words


def _read(digits: str, *, leading: bool) -> list[str]:
    if len(digits) <= _BILLION_DIGITS:
        return _below_billion(digits, leading=leading)
    head, tail = digits[:-_BILLION_DIGITS], digits[-_BILLION_DIGITS:]
    return [*_read(head, leading=leading), "tỷ", *_below_billion(tail, leading=False)]


def number_to_words(number: str) -> str:
    """Read a non-negative integer; dots and spaces are thousand separators ("1.005")."""
    digits = number.replace(".", "").replace(" ", "").lstrip("0")
    if not digits:
        return DIGITS[0]
    return " ".join(_read(digits, leading=True))


def digits_to_words(digits: str) -> str:
    """Read each digit separately, as for phone numbers: "113" -> "một một ba"."""
    if digits.startswith(COUNTRY_CODE):
        digits = "0" + digits[len(COUNTRY_CODE) :]
    return " ".join(DIGITS[int(d)] for d in digits if d.isdigit())
