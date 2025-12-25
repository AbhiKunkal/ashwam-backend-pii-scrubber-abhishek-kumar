import argparse
import json
try:
    from .pipeline import scrub_text
except ImportError:
    from pipeline import scrub_text




def main():
    parser = argparse.ArgumentParser(description="PII Scrubber CLI")
    parser.add_argument("--in", dest="input_path", required=True, help="Input JSONL file")
    parser.add_argument("--out", dest="output_path", required=True, help="Output JSONL file")
    args = parser.parse_args()

    with open(args.input_path, "r", encoding="utf-8") as fin, open(args.output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            record = json.loads(line)
            result = scrub_text(record["text"], entry_id=record.get("entry_id", "unknown"))

            fout.write(
                json.dumps({
                    "entry_id": result.entry_id,
                    "scrubbed_text": result.scrubbed_text,
                    "detected_spans": [
                        {
                            "type": s.type,
                            "start": s.start,
                            "end": s.end,
                            "confidence": s.confidence
                        }
                        for s in result.detected_spans
                    ],
                    "types_found": result.types_found
                }) + "\n"
            )


if __name__ == "__main__":
    main()
