import pandas as pd

# Load raw dataset
df = pd.read_csv("laptop_raw_data.csv")

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== FIRST 10 ROWS ==========")
print(df.head(10).to_string())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== MISSING VALUE PERCENTAGE ==========")
print((df.isnull().mean() * 100).round(2))

print("\n========== DUPLICATE ROWS ==========")
print(df.duplicated().sum())

print("\n========== UNIQUE BRANDS ==========")
print(df["Brand"].unique())

print("\n========== UNIQUE RATINGS ==========")
print(df["Rating"].unique())

print("\n========== BASIC STATISTICS ==========")
print(df.describe(include="all"))