"""Character classes shared by the normalization steps."""

import string

VIETNAMESE_LETTERS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "ỹỷỵỳựữửừứủụợỡởờớộỗổồốỏọịỉệễểềếẽẻẹặẵẳằắậẫẩầấảạươũĩđăýúùõôóòíìêéèãâàá"
    "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ"
)
WORD_CHARS = "0123456789" + VIETNAMESE_LETTERS
# A single character that is not part of a word (digits count as word characters).
NOT_WORD = r"([^0-9_" + VIETNAMESE_LETTERS + r"])"
# Same, but a following "%" or "$" also ends a date.
NOT_WORD_FOR_DATE = r"([^0-9_" + VIETNAMESE_LETTERS + r"%\$])"
# A single character that is not a letter (digits allowed).
NOT_LETTER = r"([^_" + VIETNAMESE_LETTERS + r"])"
OPENING_BRACKET_SPACE = r"([\(\[\{])(\s)"
SPACE_PUNCTUATION = r"(\s)([\.,\?\!\:\;\)\]\}])"
PUNCTUATION = set(string.punctuation) | {"\u201c", "\u2018", "\u201d", "\u2019"}  # curly quotes
