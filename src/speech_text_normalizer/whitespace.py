"""Whitespace clean-up shared by every step."""

import re

from speech_text_normalizer.symbols import OPENING_BRACKET_SPACE, SPACE_PUNCTUATION

_REPEATED_SPACE = re.compile(r"(\s)\1+")
_TABS = re.compile(r"\t+")
_SPACE_AROUND_NEWLINE = re.compile(r"[ \t]*\n[ \t]*")
_SPACE_PUNCTUATION = re.compile(SPACE_PUNCTUATION)
_OPENING_BRACKET_SPACE = re.compile(OPENING_BRACKET_SPACE)


def collapse_whitespace(text: str) -> str:
    """Squeeze repeated whitespace, drop spaces before punctuation, move spaces before brackets."""
    text = _REPEATED_SPACE.sub(r"\1", text)
    text = _SPACE_PUNCTUATION.sub(r"\2", text)
    text = _OPENING_BRACKET_SPACE.sub(r"\2\1", text)
    text = _REPEATED_SPACE.sub(r"\1", text)
    text = _SPACE_AROUND_NEWLINE.sub("\n", text)
    return _TABS.sub(" ", text).strip()


def pad(text: str) -> str:
    """Surround text with single spaces so boundary patterns match at both ends."""
    return f" {collapse_whitespace(text)} "
