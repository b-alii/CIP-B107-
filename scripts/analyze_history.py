import pandas as pd
import matplotlib.pyplot as plt

# Read historical training results
df = pd.read_csv("originals/result.csv")

print("\nAvailable columns:")
print(df.columns.tolist())

print("\nLast available records:")
print(df.tail())


# Plot training loss
if "training_loss" in df.columns:

    loss_data = df.dropna(
        subset=["training_loss"]
    )

    plt.figure()

    plt.plot(
        loss_data["step"],
        loss_data["training_loss"]
    )

    plt.xlabel("Training Step")
    plt.ylabel("Training Loss")

    plt.title("Historical Training Loss")

    plt.savefig(
        "results/historical_training_loss.png"
    )

    plt.close()


# Plot classification accuracy
if "classification/accuracy" in df.columns:

    accuracy_data = df.dropna(
        subset=["classification/accuracy"]
    )

    plt.figure()

    plt.plot(
        accuracy_data["step"],
        accuracy_data["classification/accuracy"]
    )

    plt.xlabel("Training Step")
    plt.ylabel("Accuracy")

    plt.title("Historical Classification Accuracy")

    plt.savefig(
        "results/historical_accuracy.png"
    )

    plt.close()


print("\nHistorical charts generated.")
