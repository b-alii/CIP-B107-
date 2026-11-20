
import json
import re
import csv
import ipaddress
from pathlib import Path

# Input and output file paths
INPUT_FILE = Path("originals/dataset_test.jsonl")
OUTPUT_FILE = Path("results/candidate_review.csv")

# Regex pattern for identifying possible IPv4 addresses
IP_REGEX = re.compile(
    r'(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])'
)


def validate_ipv4(candidate):
    """Check whether a candidate is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(candidate)
        return True
    except ipaddress.AddressValueError:
        return False


def get_source_label(record):
    """Extract the original label from the JSONL completion."""
    completion = str(record.get("completion", "")).strip().lower()

    if "positive" in completion:
        return "positive"
    elif "negative" in completion:
        return "negative"

    return "unknown"


def main():
    results = []

    # Check whether the input file exists
    if not INPUT_FILE.exists():
        print(f"Error: Dataset not found: {INPUT_FILE}")
        return

    # Read the JSONL dataset
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for row_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                record = json.loads(line)

            except json.JSONDecodeError as error:
                print(f"Skipping invalid JSON on line {row_number}: {error}")
                continue

            # Get the original text
            context = str(record.get("prompt", ""))

            # Get the original dataset label
            source_label = get_source_label(record)

            # Find possible IPv4 candidates
            candidates = IP_REGEX.findall(context)

            if not candidates:
                results.append({
                    "source_row": row_number,
                    "context": context,
                    "candidate": "",
                    "regex_match": False,
                    "ipv4_valid": False,
                    "source_label": source_label,
                    "analyst_note": "No IPv4 candidate found"
                })

            else:
                for candidate in candidates:

                    valid = validate_ipv4(candidate)

                    results.append({
                        "source_row": row_number,
                        "context": context,
                        "candidate": candidate,
                        "regex_match": True,
                        "ipv4_valid": valid,
                        "source_label": source_label,
                        "analyst_note": (
                            "Valid IPv4 candidate"
                            if valid
                            else "Regex match but invalid IPv4"
                        )
                    })

    # Create output directory if it does not exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Export results to CSV
    fieldnames = [
        "source_row",
        "context",
        "candidate",
        "regex_match",
        "ipv4_valid",
        "source_label",
        "analyst_note"
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Display summary
    total = len(results)
    matches = sum(row["regex_match"] for row in results)
    valid_ips = sum(row["ipv4_valid"] for row in results)
    invalid_ips = matches - valid_ips

    print("\n========== IP EXTRACTION SUMMARY ==========")
    print(f"Total output records: {total}")
    print(f"Regex matches:        {matches}")
    print(f"Valid IPv4 addresses: {valid_ips}")
    print(f"Invalid candidates:   {invalid_ips}")
    print(f"Results saved to:     {OUTPUT_FILE}")
    print("===========================================\n")


if __name__ == "__main__":
    main()
