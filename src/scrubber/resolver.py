from typing import List
from .models import Span


def resolve_overlaps(spans: List[Span]) -> List[Span]:
    """
    Resolve overlapping spans by priority and position.
    Higher priority wins. If equal priority, longer span wins.
    """
    if not spans:
        return []

    # Sort by start index, then priority desc, then length desc
    sorted_spans = sorted(
        spans,
        key=lambda s: (s.start, -s.priority, -(s.end - s.start))
    )

    resolved = []

    for span in sorted_spans:
        overlap = False
        for kept in resolved:
            if not (span.end <= kept.start or span.start >= kept.end):
                overlap = True
                break
        if not overlap:
            resolved.append(span)

    return resolved

