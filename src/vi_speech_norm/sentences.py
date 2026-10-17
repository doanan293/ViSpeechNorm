"""Split text into sentence pieces short enough for a TTS engine."""

import re

from vi_speech_norm.symbols import PUNCTUATION

_SENTENCE_END = re.compile(r"[.!?]")
_CLAUSE_END = re.compile(r"[?!.,:;-]")
_BARE_LINE_BREAK = re.compile(r"(?<![.!?])\n+")
_LINE_BREAKS = re.compile(r"\n+")


def _split_keeping_delimiters(text: str, pattern: re.Pattern[str]) -> list[str]:
    parts = pattern.split(text)
    delimiters = pattern.findall(text)
    return [
        part.strip() + delimiter for part, delimiter in zip(parts, delimiters, strict=False) if part
    ]


def _word_count(text: str) -> int:
    return len(text.split(" "))


def _combine(sentences: list[str], max_length: int) -> list[str]:
    """Greedily join neighbouring sentences while the result stays within `max_length` words."""
    combined: list[str] = []
    for sentence in sentences:
        # the original measured the pair without the joining separator
        if (
            combined
            and _word_count(combined[-1]) <= max_length
            and _word_count(combined[-1] + sentence) <= max_length
        ):
            combined[-1] = combined[-1] + " " + sentence
            continue
        combined.append(sentence)
    return combined


def _has_text(piece: str) -> bool:
    chars = set(piece)
    return not PUNCTUATION.issuperset(chars) and any(char.isalnum() for char in chars)


def _pieces(passage: str, max_length: int) -> list[str]:
    pieces: list[str] = []
    for sentence in _split_keeping_delimiters(passage, _SENTENCE_END):
        if _word_count(sentence) > max_length:
            group = _split_keeping_delimiters(sentence, _CLAUSE_END)
        else:
            group = [sentence]
        pieces.extend(piece for piece in _combine(group, max_length) if _has_text(piece))
    return pieces


def split_sentences(text: str, max_length: int = 30) -> list[str]:
    """Split text into sentence pieces of at most `max_length` words where possible."""
    text = _BARE_LINE_BREAK.sub(".\n", text)
    passages = [line.strip() for line in _LINE_BREAKS.split(text)]
    return [piece for passage in passages for piece in _pieces(passage, max_length)]
