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

DOB_REGEX = re.compile(
    r"""
    (?<!\d)
    (?:
        (?:0[1-9]|[12][0-9]|3[01])[-/](?:0[1-9]|1[0-2])[-/](?:19\d{2}|20[0-2]\d) |
        (?:19\d{2}|20[0-2]\d)[-/](?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12][0-9]|3[01])
    )
    (?!\d)
    """,
    re.VERBOSE,
)


def detect_dob(text: str) -> List[Span]:
    """
    Detect dates of birth in common formats.
    """
    spans: List[Span] = []

    for match in DOB_REGEX.finditer(text):
        spans.append(
            Span(
                type="DOB",
                start=match.start(),
                end=match.end(),
                confidence=0.85,
                priority=90,
            )
        )

    return spans
