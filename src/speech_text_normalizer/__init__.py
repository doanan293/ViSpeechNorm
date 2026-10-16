"""Normalize Vietnamese text into speakable words for text-to-speech."""

from speech_text_normalizer.passages import split_passages
from speech_text_normalizer.pipeline import STEPS, normalize
from speech_text_normalizer.sentences import split_sentences

__version__ = "0.1.0"
__all__ = ["STEPS", "__version__", "normalize", "split_passages", "split_sentences"]
