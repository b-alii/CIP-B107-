import json
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)

# Load JSONL dataset
def load_jsonl(filename):

    records = []

    with open(filename, "r", encoding="utf-8") as file:

        for line in file:

            if line.strip():
                records.append(json.loads(line))

    return records


train_data = load_jsonl(
    "originals/dataset_train.jsonl"
)

test_data = load_jsonl(
    "originals/dataset_test.jsonl"
)


# Extract prompts and labels
X_train = [item["prompt"] for item in train_data]

y_train = [
    1 if item["completion"].strip().lower() == "positive"
    else 0
    for item in train_data
]

X_test = [item["prompt"] for item in test_data]

y_test = [
    1 if item["completion"].strip().lower() == "positive"
    else 0
    for item in test_data
]


# Create machine learning pipeline
model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5)
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )

])


# Train the model
print("Training model...")

model.fit(X_train, y_train)


# Generate predictions
predictions = model.predict(X_test)


# Evaluate model
print("\nCONFUSION MATRIX")

print(
    confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )
)

print("\nCLASSIFICATION REPORT")

print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Negative", "Positive"],
        zero_division=0
    )
)

print("\nACCURACY")

print(accuracy_score(y_test, predictions))


# Save predictions
df = pd.DataFrame({

    "prompt": X_test,

    "actual": y_test,

    "predicted": predictions

})

df.to_csv(
    "results/predictions.csv",
    index=False
)

print("\nPredictions saved successfully.")
print(df.shape)
