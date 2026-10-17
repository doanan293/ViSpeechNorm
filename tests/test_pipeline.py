import pytest

from vi_speech_norm import STEPS, normalize, split_passages, split_sentences

README_INPUT = (
    "Ngày 01/02 là ngày mùng 1 Tết , tôi thêm 1 tuổi mới,cao thêm 3 cm, được lì xì 1.000.000 đồng."
)
README_OUTPUT = (
    "ngày một tháng hai là ngày mùng một tết, tôi thêm một tuổi mới, "
    "cao thêm ba xen ti mét, được lì xì một triệu đồng."
)


def test_empty_and_whitespace_input_return_empty_string() -> None:
    assert normalize("") == ""
    assert normalize("   \n\t ") == ""


def test_plain_text_is_only_lowercased() -> None:
    assert normalize("Xin chào") == "xin chào"


def test_readme_example() -> None:
    assert normalize(README_INPUT) == README_OUTPUT


def test_selected_steps_only() -> None:
    assert normalize("Có 5 cái", steps=["numbers"]) == "Có năm cái"
    assert normalize("A/B", steps=["symbols"]) == "A trên B"


def test_unknown_step_raises() -> None:
    with pytest.raises(ValueError, match="bogus"):
        normalize("x", steps=["bogus"])


def test_steps_are_listed_in_pipeline_order() -> None:
    assert STEPS[0] == "unicode"
    assert STEPS[-1] == "lowercase"
    assert STEPS.index("abbreviations") < STEPS.index("numbers")


def test_split_passages_keeps_every_paragraph() -> None:
    paragraphs = [f"Đoạn {i}. " + "Câu dài nói về chủ đề này. " * 12 for i in ("một", "hai", "ba")]
    pieces = split_passages("\n".join(paragraphs), max_length=120)
    joined = " ".join(pieces)
    assert all(f"Đoạn {i}." in joined for i in ("một", "hai", "ba"))
    assert all(len(p) <= 200 for p in pieces)


def test_split_sentences_respects_max_words() -> None:
    text = "Một hai ba bốn năm. Sáu bảy tám chín mười. Mười một mười hai."
    pieces = split_sentences(text, max_length=6)
    assert pieces[0] == "Một hai ba bốn năm."
    assert len(pieces) == 3
