import json
import re
import ipaddress
import pandas as pd

pattern = r'(?<![0-9.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9.])'


def load_jsonl(filename):

    records = []

    with open(filename, encoding="utf-8") as file:

        for line in file:

            if line.strip():
                records.append(json.loads(line))

    return records


data = load_jsonl(
    "originals/dataset_test.jsonl"
)

results = []

for item in data:

    prompt = item["prompt"]

    # Obtain original text context
    context = prompt.split(";")[0]

    candidates = re.findall(pattern, context)

    valid_ip = False

    for candidate in candidates:

        try:

            ipaddress.IPv4Address(candidate)

            valid_ip = True

        except ipaddress.AddressValueError:
            pass

    actual = (
        1 if item["completion"].strip().lower() == "positive"
        else 0
    )

    predicted = 1 if valid_ip else 0

    results.append({

        "context": context,

        "actual": actual,

        "predicted": predicted

    })


df = pd.DataFrame(results)

df.to_csv(
    "results/rule_baseline_predictions.csv",
    index=False
)

print(df.head())

print("\nBaseline results saved.")
