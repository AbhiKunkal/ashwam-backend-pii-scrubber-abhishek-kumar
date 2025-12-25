from typing import List
from .models import Span


def replace_spans(text: str, spans: List[Span]) -> str:
    """
    Replace sensitive spans in the text with [TYPE] tokens.
    Assumes spans are non-overlapping and sorted.
    """
    if not spans:
        return text

    redacted = []
    cursor = 0

    for span in spans:
        # Add text before the span
        redacted.append(text[cursor:span.start])
        # Add placeholder
        redacted.append(f"[{span.type}]")
        cursor = span.end

    # Append remaining text
    redacted.append(text[cursor:])

    return "".join(redacted)
