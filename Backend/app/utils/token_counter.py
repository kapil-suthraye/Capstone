import tiktoken

_encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    if not text:
        return 0

    return len(_encoding.encode(text))