import pytest
from src.scrubber.pipeline import scrub_text


def test_email_detection():
    text = "Contact me at test@example.com"
    result = scrub_text(text)
    assert "[EMAIL]" in result.scrubbed_text
    assert "EMAIL" in result.types_found


def test_phone_detection():
    text = "Call me on +91 98765 43210"
    result = scrub_text(text)
    assert "[PHONE]" in result.scrubbed_text


def test_dob_detection():
    text = "DOB 12/08/1995"
    result = scrub_text(text)
    assert "[DOB]" in result.scrubbed_text


def test_provider_detection():
    text = "Visited Apollo Clinic yesterday"
    result = scrub_text(text)
    assert "[PROVIDER]" in result.scrubbed_text


def test_no_false_positive_on_symptoms():
    text = "Severe headache and nausea today"
    result = scrub_text(text)
    assert "headache" in result.scrubbed_text
    assert "nausea" in result.scrubbed_text


def test_overlap_resolution():
    text = "Call me at +91 98765 43210"
    result = scrub_text(text)
    # Should only produce one PHONE, not nested replacements
    assert result.scrubbed_text.count("[PHONE]") == 1
