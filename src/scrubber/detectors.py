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
