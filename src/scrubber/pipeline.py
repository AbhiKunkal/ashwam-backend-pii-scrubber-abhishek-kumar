from typing import List
from .models import Span, EntryOutput
from .detectors import (
    detect_emails,
    detect_phone_numbers,
    detect_dob,
    detect_appointment_ids,
    detect_insurance_ids,
    detect_government_id,
    detect_provider,
    detect_address,
    detect_names,
)
from .resolver import resolve_overlaps
from .replacer import replace_spans


def scrub_text(text: str, entry_id: str = "unknown") -> EntryOutput:
    """
    Run all detectors, resolve overlaps, and return scrubbed text + metadata.
    """

    spans: List[Span] = []

    # Collect all detections
    spans.extend(detect_emails(text))
    spans.extend(detect_phone_numbers(text))
    spans.extend(detect_dob(text))
    spans.extend(detect_appointment_ids(text))
    spans.extend(detect_insurance_ids(text))
    spans.extend(detect_government_id(text))
    spans.extend(detect_provider(text))
    spans.extend(detect_address(text))
    spans.extend(detect_names(text))

    # Resolve conflicts
    resolved = resolve_overlaps(spans)

    # Replace text
    scrubbed_text = replace_spans(text, resolved)

    return EntryOutput(
        entry_id=entry_id,
        scrubbed_text=scrubbed_text,
        detected_spans=resolved,
        types_found=sorted({s.type for s in resolved}),
    )
