"""Normalize Vietnamese text into speakable words for text-to-speech."""

from vi_speech_norm.passages import split_passages
from vi_speech_norm.pipeline import STEPS, normalize
from vi_speech_norm.sentences import split_sentences

__version__ = "0.1.0"
__all__ = ["STEPS", "__version__", "normalize", "split_passages", "split_sentences"]
