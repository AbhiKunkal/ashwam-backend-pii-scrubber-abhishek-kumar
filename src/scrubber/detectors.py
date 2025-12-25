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

APPOINTMENT_ID_REGEX = re.compile(
    r"""
    \b
    (?:APPT|APT|BKG|BOOK|REF|REFERRAL|INV)
    [\-_]?
    [A-Z0-9]{4,}
    \b
    """,
    re.VERBOSE | re.IGNORECASE,
)


def detect_appointment_ids(text: str) -> List[Span]:
    """
    Detect appointment / booking / referral identifiers.
    """
    spans: List[Span] = []

    for match in APPOINTMENT_ID_REGEX.finditer(text):
        spans.append(
            Span(
                type="APPOINTMENT_ID",
                start=match.start(),
                end=match.end(),
                confidence=0.9,
                priority=88,
            )
        )

    return spans
INSURANCE_ID_REGEX = re.compile(
    r"""
    \b
    (?:INS|INSURANCE|POLICY|POL|BUPA)
    [-_ ]?
    [A-Z0-9]{4,}
    \b
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_insurance_ids(text: str) -> List[Span]:
    """
    Detect insurance or policy identifiers.
    """
    spans: List[Span] = []

    for match in INSURANCE_ID_REGEX.finditer(text):
        spans.append(
            Span(
                type="INSURANCE_ID",
                start=match.start(),
                end=match.end(),
                confidence=0.9,
                priority=87,
            )
        )

    return spans
PROVIDER_REGEX = re.compile(
    r"""
    (?:
        (?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})   # Capitalized name parts
        \s+
        (?:Clinic|Hospital|Centre|Center|Lab|Laboratory|Health|Healthcare|Medical)
    )
    """,
    re.VERBOSE,
)


def detect_provider(text: str) -> List[Span]:
    """
    Detect healthcare provider or clinic names.
    """
    spans: List[Span] = []

    for match in PROVIDER_REGEX.finditer(text):
        spans.append(
            Span(
                type="PROVIDER",
                start=match.start(),
                end=match.end(),
                confidence=0.8,
                priority=70,
            )
        )

    return spans
ADDRESS_REGEX = re.compile(
    r"""
    \b
    \d{1,4}                       # street number
    \s+
    (?:[A-Z][a-z]+(?:\s+|$)){1,4} # street name words
    (?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd|Drive|Dr)
    \b
    """,
    re.VERBOSE,
)


def detect_address(text: str) -> List[Span]:
    """
    Detect street-style addresses.
    """
    spans: List[Span] = []

    for match in ADDRESS_REGEX.finditer(text):
        spans.append(
            Span(
                type="ADDRESS",
                start=match.start(),
                end=match.end(),
                confidence=0.85,
                priority=70,
            )
        )

    return spans

NAME_REGEX = re.compile(
    r"""
    (?:
        (?:Dr\.?|Mr\.?|Ms\.?|Mrs\.?|Patient|Partner)\s+
        (?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})
    )
    """,
    re.VERBOSE,
)


def detect_names(text: str) -> List[Span]:
    """
    Detect personal names with honorifics or roles.
    """
    spans: List[Span] = []

    for match in NAME_REGEX.finditer(text):
        spans.append(
            Span(
                type="NAME",
                start=match.start(),
                end=match.end(),
                confidence=0.7,
                priority=60,
            )
        )

    return spans

GOV_ID_REGEX = re.compile(
    r"""
    (
        \b\d{3}-\d{2}-\d{4}\b               # US SSN style
        |
        \b\d{4}\s\d{4}\s\d{4}\b             # Aadhaar style
        |
        \b(?:GOV|ID|SSN|AADHAAR)[\s:-]?\d{4,}\b
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def detect_government_id(text: str) -> List[Span]:
    """
    Detect government-issued identifiers (SSN, Aadhaar, etc.)
    """
    spans: List[Span] = []

    for match in GOV_ID_REGEX.finditer(text):
        spans.append(
            Span(
                type="GOVERNMENT_ID",
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                priority=95,
            )
        )

    return spans
