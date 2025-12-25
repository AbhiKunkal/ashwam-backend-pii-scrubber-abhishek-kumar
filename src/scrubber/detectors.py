import re
from typing import List

from .models import Span


EMAIL_REGEX = re.compile(
    r"""
    \b
    [a-zA-Z0-9._%+-]+      # local part
    @
    [a-zA-Z0-9.-]+        # domain
    \.
    [a-zA-Z]{2,}          # TLD
    \b
    """,
    re.VERBOSE
)


def detect_emails(text: str) -> List[Span]:
    """
    Detect email addresses in text.
    """
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
PHONE_REGEX = re.compile(
    r"""
    (?<!\w)
    (\+?\d{1,3}[\s-]?)?
    (\(?\d{2,4}\)?[\s-]?)?
    \d{3,4}[\s-]?\d{4}
    (?!\w)
    """,
    re.VERBOSE
)


PHONE_REGEX = re.compile(
    r"""
    (?<!\w)
    (?:\+?\d{1,3}[\s\-]?)?      # optional country code
    (?:\(?\d{2,4}\)?[\s\-]?)?   # optional area code
    \d{3,5}[\s\-]?\d{4}         # local number
    (?!\w)
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


def detect_phone_numbers(text: str) -> List[Span]:
    """
    Detect phone numbers while avoiding false positives
    such as dates, weights, or step counts.
    """
    spans: List[Span] = []

    for match in PHONE_REGEX.finditer(text):
        candidate = match.group()

        # Keep digits only
        digits = re.sub(r"\D", "", candidate)

        # Guardrails
        if len(digits) < 10 or len(digits) > 15:
            continue

        # Avoid measurements / dates
        window = text[match.end():match.end() + 6].lower()
        if any(x in window for x in ["kg", "kgs", "bpm", "steps", "/"]):
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


