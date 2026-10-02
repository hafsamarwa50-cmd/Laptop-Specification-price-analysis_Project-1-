import pandas as pd
import numpy as np


# ==========================================
# LOAD CLEANED DATA
# ==========================================

df = pd.read_csv("laptop_cleaned_data.csv")


print("\n===================================")
print("LAPTOP DATASET - EDA")
print("===================================")


# ==========================================
# 1. DATASET SHAPE
# ==========================================

print("\n========== DATASET SHAPE ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 2. COLUMN NAMES
# ==========================================

print("\n========== COLUMN NAMES ==========")

print(df.columns.tolist())


# ==========================================
# 3. DATA TYPES
# ==========================================

print("\n========== DATA TYPES ==========")

print(df.dtypes)


# ==========================================
# 4. MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


# ==========================================
# 5. DUPLICATES
# ==========================================

print("\n========== DUPLICATES ==========")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)


# ==========================================
# 6. NUMERICAL SUMMARY
# ==========================================

print("\n========== NUMERICAL SUMMARY ==========")

print(
    df[
        [
            "Price",
            "RAM_GB",
            "Screen_Size_Inches"
        ]
    ].describe()
)


# ==========================================
# 7. BRAND DISTRIBUTION
# ==========================================

print("\n========== BRAND DISTRIBUTION ==========")

print(
    df["Brand"].value_counts()
)


# ==========================================
# 8. PRICE CATEGORY DISTRIBUTION
# ==========================================

print("\n========== PRICE CATEGORY ==========")

print(
    df["Price_Category"].value_counts()
)


# ==========================================
# 9. RAM DISTRIBUTION
# ==========================================

print("\n========== RAM DISTRIBUTION ==========")

print(
    df["RAM_GB"].value_counts().sort_index()
)


# ==========================================
# 10. CPU FAMILY DISTRIBUTION
# ==========================================

print("\n========== CPU FAMILY ==========")

print(
    df["CPU_Family"].value_counts()
)


# ==========================================
# 11. STORAGE TYPE DISTRIBUTION
# ==========================================

print("\n========== STORAGE TYPE ==========")

print(
    df["Storage_Type"].value_counts()
)


# ==========================================
# 12. GPU TYPE DISTRIBUTION
# ==========================================

print("\n========== GPU TYPE ==========")

print(
    df["GPU_Type"].value_counts()
)


# ==========================================
# 13. OPERATING SYSTEM DISTRIBUTION
# ==========================================

print("\n========== OPERATING SYSTEM ==========")

print(
    df["Operating_System"].value_counts()
)


# ==========================================
# 14. PRICE STATISTICS
# ==========================================

print("\n========== PRICE STATISTICS ==========")

print(
    "Minimum price:",
    df["Price"].min()
)

print(
    "Maximum price:",
    df["Price"].max()
)

print(
    "Average price:",
    round(df["Price"].mean(), 2)
)

print(
    "Median price:",
    round(df["Price"].median(), 2)
)


# ==========================================
# 15. RAM STATISTICS
# ==========================================

print("\n========== RAM STATISTICS ==========")

print(
    "Minimum RAM:",
    df["RAM_GB"].min(),
    "GB"
)

print(
    "Maximum RAM:",
    df["RAM_GB"].max(),
    "GB"
)

print(
    "Average RAM:",
    round(df["RAM_GB"].mean(), 2),
    "GB"
)


# ==========================================
# 16. SCREEN SIZE STATISTICS
# ==========================================

print("\n========== SCREEN SIZE STATISTICS ==========")

print(
    "Minimum screen size:",
    df["Screen_Size_Inches"].min()
)

print(
    "Maximum screen size:",
    df["Screen_Size_Inches"].max()
)

print(
    "Average screen size:",
    round(
        df["Screen_Size_Inches"].mean(),
        2
    )
)


# ==========================================
# 17. AVERAGE PRICE BY BRAND
# ==========================================

print("\n========== AVERAGE PRICE BY BRAND ==========")

brand_price = (
    df.groupby("Brand")["Price"]
    .mean()
    .sort_values(ascending=False)
)

print(
    brand_price.round(2)
)


# ==========================================
# 18. AVERAGE PRICE BY RAM
# ==========================================

print("\n========== AVERAGE PRICE BY RAM ==========")

ram_price = (
    df.groupby("RAM_GB")["Price"]
    .mean()
    .sort_index()
)

print(
    ram_price.round(2)
)


# ==========================================
# 19. AVERAGE PRICE BY CPU FAMILY
# ==========================================

print("\n========== AVERAGE PRICE BY CPU FAMILY ==========")

cpu_price = (
    df.groupby("CPU_Family")["Price"]
    .mean()
    .sort_values(ascending=False)
)

print(
    cpu_price.round(2)
)


# ==========================================
# 20. AVERAGE PRICE BY STORAGE TYPE
# ==========================================

print("\n========== AVERAGE PRICE BY STORAGE TYPE ==========")

storage_price = (
    df.groupby("Storage_Type")["Price"]
    .mean()
    .sort_values(ascending=False)
)

print(
    storage_price.round(2)
)


print("\n===================================")
print("EDA COMPLETED")
print("===================================")