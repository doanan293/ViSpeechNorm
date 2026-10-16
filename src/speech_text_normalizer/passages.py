import re


def split_text_passages(text, regex, include_split_chars, strip_chars):
    if include_split_chars:
        return [e.strip(strip_chars) + d for e, d in zip(re.split(regex, text), re.findall(regex, text)) if e]
    else:
        return [e.strip(strip_chars) for e in re.split(regex, text)]

def combine_passages(passages: list, maxLength: int) -> list:
    if len(passages) <= 1:
        return passages
    if len(passages[0]) >= maxLength:
        return [passages[0]] + combine_passages(passages[1:], maxLength=maxLength)

    if len(passages[0] + passages[1]) <= maxLength:
        return combine_passages([passages[0] + "\n" + passages[1]]+passages[2:], maxLength=maxLength)
    else:
        return [passages[0]] + combine_passages(passages[1:], maxLength=maxLength)

def split_long_passages(passages: list, maxLength: int) -> list:
    sub_passages = []
    for passage in passages:
        if len(passage) > maxLength:
            sub_passages.append(split_text_passages(passage,  r'[.!?]', True, ' '))
        else:
            sub_passages.append([passage])
    return sub_passages

def split_passages(text: str, max_length: int = 1000) -> list[str]:
    """Split text into passages no longer than `max_length` characters where possible."""
    passages = [p for p in split_text_passages(text, r"[\n]+", False, "\n\t ") if p]
    pieces = [piece for group in split_long_passages(passages, max_length) for piece in combine_passages(group, max_length)]
    return combine_passages(pieces, max_length)
