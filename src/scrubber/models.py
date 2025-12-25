from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Span:
    """
    Represents a detected sensitive identifier span
    in the original text.
    """
    type: str
    start: int
    end: int
    confidence: float
    priority: int


@dataclass
class EntryOutput:
    """
    Represents the scrubbed output for a single journal entry.
    """
    entry_id: str
    scrubbed_text: str
    detected_spans: List[Span]
    types_found: List[str]
    scrubber_version: str = "v1"

