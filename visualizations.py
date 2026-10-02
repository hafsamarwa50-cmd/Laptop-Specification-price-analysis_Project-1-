import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# LOAD CLEANED DATA
# ============================================================

df = pd.read_csv("laptop_cleaned_data.csv")


print("===================================")
print("LAPTOP DATA VISUALIZATION")
print("===================================")


# ============================================================
# CHART 1 — LAPTOP COUNT BY BRAND
# ============================================================

plt.figure(figsize=(10, 6))

brand_counts = df["Brand"].value_counts()

brand_counts.plot(kind="bar")

plt.title("Number of Laptops by Brand")
plt.xlabel("Brand")
plt.ylabel("Number of Laptops")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 2 — PRICE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["Price"],
    bins=15,
    edgecolor="black"
)

plt.title("Laptop Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Laptops")
plt.tight_layout()
plt.show()


# ============================================================
# CHART 3 — AVERAGE PRICE BY BRAND
# ============================================================

plt.figure(figsize=(10, 6))

brand_price = (
    df.groupby("Brand")["Price"]
    .mean()
    .sort_values(ascending=False)
)

brand_price.plot(kind="bar")

plt.title("Average Laptop Price by Brand")
plt.xlabel("Brand")
plt.ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 4 — PRICE CATEGORY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 6))

price_category = df["Price_Category"].value_counts()

price_category.plot(
    kind="bar"
)

plt.title("Laptop Price Category Distribution")
plt.xlabel("Price Category")
plt.ylabel("Number of Laptops")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 5 — RAM DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 6))

ram_counts = (
    df["RAM_GB"]
    .value_counts()
    .sort_index()
)

ram_counts.plot(kind="bar")

plt.title("Laptop Distribution by RAM")
plt.xlabel("RAM (GB)")
plt.ylabel("Number of Laptops")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 6 — AVERAGE PRICE BY RAM
# ============================================================

plt.figure(figsize=(8, 6))

ram_price = (
    df.groupby("RAM_GB")["Price"]
    .mean()
    .sort_index()
)

ram_price.plot(
    kind="bar"
)

plt.title("Average Laptop Price by RAM")
plt.xlabel("RAM (GB)")
plt.ylabel("Average Price")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 7 — CPU FAMILY DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

cpu_counts = (
    df["CPU_Family"]
    .value_counts()
)

cpu_counts.plot(kind="bar")

plt.title("Laptop Distribution by CPU Family")
plt.xlabel("CPU Family")
plt.ylabel("Number of Laptops")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 8 — AVERAGE PRICE BY CPU FAMILY
# ============================================================

plt.figure(figsize=(10, 6))

cpu_price = (
    df.groupby("CPU_Family")["Price"]
    .mean()
    .sort_values(ascending=False)
)

cpu_price.plot(kind="bar")

plt.title("Average Laptop Price by CPU Family")
plt.xlabel("CPU Family")
plt.ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 9 — STORAGE TYPE DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

storage_counts = (
    df["Storage_Type"]
    .value_counts()
)

storage_counts.plot(kind="bar")

plt.title("Laptop Distribution by Storage Type")
plt.xlabel("Storage Type")
plt.ylabel("Number of Laptops")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# ============================================================
# CHART 10 — SCREEN SIZE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["Screen_Size_Inches"],
    bins=10,
    edgecolor="black"
)

plt.title("Laptop Screen Size Distribution")
plt.xlabel("Screen Size (Inches)")
plt.ylabel("Number of Laptops")
plt.tight_layout()
plt.show()


# ============================================================
# COMPLETED
# ============================================================

print("\n===================================")
print("10 VISUALIZATIONS COMPLETED")
print("===================================")