import pandas as pd

# Load the original dataset
df = pd.read_csv("originals/dataset_small.csv")

# Display basic information
print("\nDATASET OVERVIEW")
print("================")

print("\nNumber of records:")
print(len(df))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())
