


# PII / Sensitive Identifier Scrubber

A lightweight, deterministic system for detecting and masking personally identifiable information (PII) in free-text health journal entries.  
Designed to preserve clinical meaning while removing sensitive data.

---

## Overview

This project implements a rule-based PII scrubber that detects and replaces sensitive identifiers such as emails, phone numbers, addresses, and health identifiers from unstructured text.

The system is designed to be:
- Deterministic and explainable
- Safe for healthcare-related text
- Easy to test and extend

---

## Supported Identifier Types

### Direct Identifiers
- **EMAIL**
- **PHONE** (supports AU / US / IN formats)
- **NAME** (heuristic)
- **ADDRESS**
- **DATE OF BIRTH (DOB)**

### Health-System Identifiers
- **PROVIDER / CLINIC**
- **APPOINTMENT / BOOKING ID**
- **INSURANCE / POLICY ID**
- **GOVERNMENT ID** (e.g., Aadhaar / SSN-style patterns)

---

## What Is Not Removed
To preserve clinical meaning, the system intentionally **does not scrub**:
- Symptoms (e.g., cramps, nausea)
- Vitals (e.g., BP, weight)
- Medications
- Activity or lifestyle information

---

## How It Works

## Detection Approach

- Rule-based pattern matching using regular expressions
- Conservative heuristics to reduce false positives
- Priority-based conflict resolution when patterns overlap
- Deterministic behavior for reproducibility

---

## Overlap Resolution Strategy

When multiple identifiers overlap:
1. Higher-priority entity types take precedence
2. Longer matches override shorter ones
3. Only one replacement is applied per span

This ensures clean and predictable output.

### Replacement Logic

The `replacer.py` module applies the final transformation step by replacing
detected sensitive spans with standardized placeholders (e.g. `[EMAIL]`,
`[PHONE]`, `[DOB]`).

It operates after span detection and resolution, ensuring that:
- Replacements do not overlap
- Original text structure is preserved
- Only confirmed spans are modified







## Output Format

Each processed record produces:

```json
{
  "entry_id": "j_001",
  "scrubbed_text": "Contact me at [EMAIL]",
  "detected_spans": [
    {
      "type": "EMAIL",
      "start": 14,
      "end": 32,
      "confidence": 0.95
    }
  ],
  "types_found": ["EMAIL"],
  "scrubber_version": "v1"
}


```

## Project Structure

```

src/
scrubber/
cli.py          # CLI entrypoint
pipeline.py     # Orchestration logic
detectors.py    # Pattern detection
replacer.py     # Applies replacements
resolver.py     # Overlap resolution
models.py       # Shared data structures

tests/
test_scrubber.py

sample_data/
journals.jsonl

````

---

## Running the Scrubber

```bash
python -m src.scrubber.cli --in journals.jsonl --out scrubbed.jsonl
````

---

## Running Tests

```bash
PYTHONPATH=src pytest
```
Tests validate:

All required identifier types are detected

No over-scrubbing of health information

Overlapping patterns resolve correctly

---

## Design Decisions

* **Rule-based approach** chosen for determinism and auditability.
* **Overlapping matches resolved** using priority + span length.
* **Conservative matching** to avoid accidental redaction of medical context.
* No external ML dependencies to keep behavior predictable.

---

## Limitations

* Name detection is heuristic and may miss uncommon formats.
* Address detection is pattern-based and not geocoded.
* Does not use NLP models; focuses on precision over recall.

---

## Future Improvements

* Add optional ML-based NER layer
* Expand international address patterns
* Add confidence scoring calibration
* Add structured evaluation metrics

---

## Summary

This project demonstrates a clean, auditable, and privacy-first approach to detecting sensitive information in health-related free text.
It prioritizes correctness, transparency, and safety over aggressive redaction.

---

**Author:**
Abhishek Kumar



