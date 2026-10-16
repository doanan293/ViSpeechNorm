"""Load the lookup tables shipped in speech_text_normalizer/data/."""

import tomllib
from functools import cache
from importlib.resources import files
from typing import cast


@cache
def table(file: str, section: str) -> dict[str, str]:
    raw = tomllib.loads(files("speech_text_normalizer").joinpath("data", file).read_text("utf-8"))
    return cast("dict[str, str]", raw[section])


@cache
def word_list(file: str, section: str, key: str) -> tuple[str, ...]:
    raw = tomllib.loads(files("speech_text_normalizer").joinpath("data", file).read_text("utf-8"))
    return tuple(cast("list[str]", raw[section][key]))
