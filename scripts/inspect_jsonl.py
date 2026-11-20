import json
from collections import Counter

files = [
    "originals/dataset_train.jsonl",
    "originals/dataset_test.jsonl"
]

for filename in files:

    labels = Counter()
    total = 0

    print(f"\nInspecting: {filename}")

    with open(filename, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                record = json.loads(line)
                total += 1

                completion = record.get("completion", "").strip()
                labels[completion] += 1

            except json.JSONDecodeError:
                print(f"Invalid JSON at line {line_number}")

    print("Total records:", total)
    print("Label distribution:", labels)
