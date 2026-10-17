"""Load the lookup tables shipped in vi_speech_norm/data/."""

import tomllib
from functools import cache
from importlib.resources import files
from typing import cast


@cache
def table(file: str, section: str) -> dict[str, str]:
    raw = tomllib.loads(files("vi_speech_norm").joinpath("data", file).read_text("utf-8"))
    return cast("dict[str, str]", raw[section])


@cache
def word_list(file: str, section: str, key: str) -> tuple[str, ...]:
    raw = tomllib.loads(files("vi_speech_norm").joinpath("data", file).read_text("utf-8"))
    return tuple(cast("list[str]", raw[section][key]))
