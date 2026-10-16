"""Whitespace clean-up shared by every step."""

import re

from speech_text_normalizer.symbols import (
    opening_brackets_and_punctutations_re,
    punctutations_re,
)

_REPEATED_SPACE = re.compile(r"(\s)\1+")
_TABS = re.compile(r"\t+")


def _before_punctuation(match: re.Match[str]) -> str:
    return match.group(2)


def _after_bracket(match: re.Match[str]) -> str:
    return match.group(2) + match.group(1)


def collapse_whitespace(text: str) -> str:
    """Squeeze repeated whitespace and drop spaces before punctuation or after brackets."""
    text = _REPEATED_SPACE.sub(r"\1", text)
    text = re.sub(punctutations_re, _before_punctuation, text)
    text = re.sub(opening_brackets_and_punctutations_re, _after_bracket, text)
    text = _REPEATED_SPACE.sub(r"\1", text)
    return _TABS.sub(" ", text).strip()


def pad(text: str) -> str:
    """Surround text with single spaces so word-boundary patterns match at both ends."""
    return f" {collapse_whitespace(text)} "
