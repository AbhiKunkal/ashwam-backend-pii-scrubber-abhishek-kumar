import re
from typing import List

from .models import Span


EMAIL_REGEX = re.compile(
    r"""
    \b
    [a-zA-Z0-9._%+-]+
    @
    [a-zA-Z0-9.-]+
    \.
    [a-zA-Z]{2,}
    \b
    """,
    re.VERBOSE
)


PHONE_REGEX = re.compile(
    r"""
    (?<!\w)
    (\+?\d[\d\s\-()]{7,}\d)
    (?!\w)
    """,
    re.VERBOSE
)


def detect_emails(text: str) -> List[Span]:
    """Detect email addresses in text."""
    spans: List[Span] = []

    for match in EMAIL_REGEX.finditer(text):
        spans.append(
            Span(
                type="EMAIL",
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                priority=80,
            )
        )

    return spans


def detect_phone_numbers(text: str) -> List[Span]:
    """Detect phone numbers while avoiding false positives."""
    spans: List[Span] = []

    for match in PHONE_REGEX.finditer(text):
        candidate = match.group()
        digits = re.sub(r"\D", "", candidate)

        # Reject too-short or unrealistic numbers
        if len(digits) < 10 or len(digits) > 15:
            continue

        # Avoid health metrics
        trailing = text[match.end():match.end() + 6].lower()
        if any(x in trailing for x in ("kg", "kgs", "bpm", "steps", "/")):
            continue

        spans.append(
            Span(
                type="PHONE",
                start=match.start(),
                end=match.end(),
                confidence=0.9,
                priority=75,
            )
        )

    return spans
