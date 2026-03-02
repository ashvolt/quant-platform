import pandas as pd

df = pd.read_parquet("data/processed/features/BTCUSDT/features.parquet")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nHead:")
print(df.head())