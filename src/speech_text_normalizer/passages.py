"""Split long text into passages of bounded character length."""

import re

_LINE_BREAKS = re.compile(r"[\n]+")
_SENTENCE_END = re.compile(r"[.!?]")


def _sentences(passage: str) -> list[str]:
    parts = _SENTENCE_END.split(passage)
    delimiters = _SENTENCE_END.findall(passage)
    return [
        part.strip(" ") + delimiter
        for part, delimiter in zip(parts, delimiters, strict=False)
        if part
    ]


def _combine(passages: list[str], max_length: int) -> list[str]:
    """Greedily join neighbouring passages with a newline while they fit in `max_length`."""
    combined: list[str] = []
    for passage in passages:
        # the original measured the pair without the joining separator
        if (
            combined
            and len(combined[-1]) < max_length
            and len(combined[-1] + passage) <= max_length
        ):
            combined[-1] = combined[-1] + "\n" + passage
            continue
        combined.append(passage)
    return combined


def split_passages(text: str, max_length: int = 1000) -> list[str]:
    """Split text into passages no longer than `max_length` characters where possible."""
    passages = [p for p in (part.strip("\n\t ") for part in _LINE_BREAKS.split(text)) if p]
    pieces: list[str] = []
    for passage in passages:
        group = _sentences(passage) if len(passage) > max_length else [passage]
        pieces.extend(_combine(group, max_length))
    return _combine(pieces, max_length)
