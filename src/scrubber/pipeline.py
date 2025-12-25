from typing import List
from .models import Span, EntryOutput
from .detectors import detect_emails, detect_phone_numbers, detect_dob
from .resolver import resolve_overlaps


def scrub_text(text: str, entry_id: str = "unknown") -> EntryOutput:
    """
    Run all detectors, resolve overlaps, and return redacted output.
    """

    spans: List[Span] = []

    # Run detectors
    spans.extend(detect_emails(text))
    spans.extend(detect_phone_numbers(text))
    spans.extend(detect_dob(text))

    # Resolve overlaps
    resolved = resolve_overlaps(spans)

    # Sort spans left to right
    resolved.sort(key=lambda s: s.start)

    # Build redacted text
    redacted = []
    last_idx = 0

    for span in resolved:
        redacted.append(text[last_idx:span.start])
        redacted.append(f"[{span.type}]")
        last_idx = span.end

    redacted.append(text[last_idx:])

    return EntryOutput(
        entry_id=entry_id,
        scrubbed_text="".join(redacted),
        detected_spans=resolved,
        types_found=list({s.type for s in resolved}),
    )
