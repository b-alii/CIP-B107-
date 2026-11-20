import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    accuracy_score
)

df = pd.read_csv("results/predictions.csv")

actual = df["actual"]
predicted = df["predicted"]

cm = confusion_matrix(
    actual,
    predicted,
    labels=[0, 1]
)

print("\nCONFUSION MATRIX")
print(cm)

print("\nCLASSIFICATION REPORT")

print(
    classification_report(
        actual,
        predicted,
        target_names=["Negative", "Positive"],
        zero_division=0
    )
)

print("\nACCURACY:", accuracy_score(actual, predicted))


# Visualize confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Negative", "Positive"]
)

display.plot()

plt.title("IP Evidence Classification Confusion Matrix")

plt.savefig(
    "results/confusion_matrix.png"
)

plt.close()
