from pathlib import Path

from speech_text_normalizer import normalize

GOLDEN = Path(__file__).parent / "golden"


def test_paragraph_matches_reviewed_output() -> None:
    text = (GOLDEN / "paragraph.txt").read_text(encoding="utf-8")
    expected = (GOLDEN / "paragraph.expected.txt").read_text(encoding="utf-8").strip()
    assert normalize(text) == expected
