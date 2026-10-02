import pandas as pd
import numpy as np
import re


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

df = pd.read_csv("laptop_raw_data.csv")

print("\n========== RAW DATA ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)


# ============================================================
# 3. REMOVE DUPLICATE ROWS
# ============================================================

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows found:", duplicate_count)

df = df.drop_duplicates().copy()


# ============================================================
# 4. CLEAN BRAND
# ============================================================

df["Brand"] = (
    df["Brand"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)


# Recover missing brands from model names
def identify_brand(row):

    current_brand = row["Brand"]
    model = str(row["Model"]).lower()

    if current_brand != "Unknown":
        return current_brand

    brand_keywords = {
        "Acer": [
            "aspire",
            "acer"
        ],

        "Lenovo": [
            "thinkpad",
            "ideapad",
            "lenovo",
            "yoga"
        ],

        "HP": [
            "probook",
            "pavilion",
            "elitebook",
            "hp"
        ],

        "Dell": [
            "inspiron",
            "latitude",
            "xps",
            "dell"
        ],

        "Asus": [
            "asus",
            "vivobook",
            "zenbook"
        ],

        "Toshiba": [
            "toshiba",
            "satellite"
        ],

        "Apple": [
            "macbook",
            "apple"
        ],

        "MSI": [
            "msi"
        ],

        "Packard": [
            "packard"
        ]
    }

    for brand, keywords in brand_keywords.items():

        for keyword in keywords:

            if keyword in model:
                return brand

    return "Unknown"


df["Brand"] = df.apply(
    identify_brand,
    axis=1
)


# Standardize brand names
df["Brand"] = (
    df["Brand"]
    .replace({
        "Hp": "HP",
        "hp": "HP",
        "H.p": "HP",
        "PACKARD": "Packard",
        "DELL": "Dell",
        "ACER": "Acer",
        "ASUS": "Asus",
        "LENOVO": "Lenovo",
        "TOSHIBA": "Toshiba",
        "APPLE": "Apple",
        "MSI": "MSI"
    })
)


# ============================================================
# 5. CLEAN MODEL
# ============================================================

df["Model"] = (
    df["Model"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 6. CLEAN PRICE
# ============================================================

df["Price"] = (
    df["Price"]
    .astype(str)
    .str.replace(r"[^0-9.]", "", regex=True)
)

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)


# ============================================================
# 7. CLEAN RAM
# ============================================================

df["RAM_GB"] = pd.to_numeric(
    df["RAM_GB"],
    errors="coerce"
)


# ============================================================
# 8. CLEAN SCREEN SIZE
# ============================================================

df["Screen_Size_Inches"] = pd.to_numeric(
    df["Screen_Size_Inches"],
    errors="coerce"
)


# ============================================================
# 9. EXTRACT CPU FROM DESCRIPTION
# ============================================================

def extract_cpu(text):

    if pd.isna(text):
        return np.nan

    text = str(text)

    cpu_patterns = [
        r"(Core i[3579]-[A-Za-z0-9]+)",
        r"(Core i[3579]\s+\d+(?:\.\d+)?GHz)",
        r"(Core i[3579])",
        r"(AMD E\d?-\d+[A-Za-z0-9\-]*)",
        r"(AMD A\d+-\d+[A-Za-z0-9\-]*)",
        r"(Ryzen\s+\d+[A-Za-z0-9\-]*)",
        r"(Pentium\s+[A-Za-z0-9\-]+)",
        r"(Celeron\s+[A-Za-z0-9\-]+)",
        r"(Atom\s+[A-Za-z0-9\-]+)"
    ]

    for pattern in cpu_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return np.nan


df["CPU"] = df["Description"].apply(
    extract_cpu
)


# ============================================================
# 10. CREATE CPU FAMILY
# ============================================================

def cpu_family(cpu):

    if pd.isna(cpu):
        return "Unknown"

    cpu = str(cpu).lower()

    if "core i9" in cpu:
        return "Intel Core i9"

    elif "core i7" in cpu:
        return "Intel Core i7"

    elif "core i5" in cpu:
        return "Intel Core i5"

    elif "core i3" in cpu:
        return "Intel Core i3"

    elif "pentium" in cpu:
        return "Intel Pentium"

    elif "celeron" in cpu:
        return "Intel Celeron"

    elif "atom" in cpu:
        return "Intel Atom"

    elif "ryzen" in cpu:
        return "AMD Ryzen"

    elif "amd e" in cpu:
        return "AMD E-Series"

    elif "amd a" in cpu:
        return "AMD A-Series"

    else:
        return "Other"


df["CPU_Family"] = df["CPU"].apply(
    cpu_family
)


# ============================================================
# 11. EXTRACT STORAGE FROM DESCRIPTION
# ============================================================

def extract_storage(text):

    if pd.isna(text):
        return np.nan

    text = str(text)

    # Find storage values such as:
    # 500GB
    # 750GB
    # 1TB
    # 240GB SSD
    # 128GB SSD

    pattern = (
        r"\b"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"(TB|GB)"
        r"(?:\s*(SSD|HDD))?"
        r"\b"
    )

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    storage_values = []

    for number, unit, storage_type in matches:

        number_value = float(number)

        # Ignore values that are most likely RAM.
        # Storage values below 64 GB are excluded.
        if unit.upper() == "GB" and number_value < 64:
            continue

        value = f"{number}{unit.upper()}"

        if storage_type:
            value += f" {storage_type.upper()}"

        storage_values.append(value)

    # Remove duplicates while preserving order
    storage_values = list(
        dict.fromkeys(storage_values)
    )

    if storage_values:
        return " + ".join(storage_values)

    return np.nan


df["Storage"] = df["Description"].apply(
    extract_storage
)


# ============================================================
# 12. CREATE STORAGE TYPE
# ============================================================

def storage_type(storage):

    if pd.isna(storage):
        return "Unknown"

    storage = str(storage).upper()

    if "SSD" in storage and "HDD" in storage:
        return "SSD + HDD"

    elif "SSD" in storage:
        return "SSD"

    elif "HDD" in storage:
        return "HDD"

    else:
        return "HDD/Unspecified"


df["Storage_Type"] = df["Storage"].apply(
    storage_type
)


# ============================================================
# 13. EXTRACT GPU FROM DESCRIPTION
# ============================================================

def extract_gpu(text):

    if pd.isna(text):
        return np.nan

    text = str(text)

    gpu_patterns = [

        r"(Radeon\s+[A-Za-z0-9\-\s]+)",

        r"(GeForce\s+[A-Za-z0-9\-\s]+)",

        r"(NVIDIA\s+[A-Za-z0-9\-\s]+)",

        r"(Intel\s+(?:HD|UHD|Iris)[A-Za-z0-9\-\s]*)"
    ]

    for pattern in gpu_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            gpu = match.group(1)

            # Stop at comma
            gpu = gpu.split(",")[0]

            return gpu.strip()

    return np.nan


df["GPU"] = df["Description"].apply(
    extract_gpu
)


# ============================================================
# 14. CREATE GPU TYPE
# ============================================================

def gpu_type(gpu):

    if pd.isna(gpu):
        return "Unknown"

    gpu = str(gpu).lower()

    if "radeon" in gpu:
        return "AMD Radeon"

    elif "geforce" in gpu or "nvidia" in gpu:
        return "NVIDIA"

    elif "intel" in gpu:
        return "Intel Integrated"

    else:
        return "Other"


df["GPU_Type"] = df["GPU"].apply(
    gpu_type
)


# ============================================================
# 15. CLEAN OPERATING SYSTEM
# ============================================================

df["Operating_System"] = (
    df["Operating_System"]
    .replace("nan", np.nan)
    .fillna("Unknown")
    .astype(str)
    .str.strip()
)


def standardize_os(os_name):

    os_name = str(os_name).lower()

    if "windows 11" in os_name:
        return "Windows 11"

    elif "windows 10" in os_name or "win10" in os_name:
        return "Windows 10"

    elif "windows 8" in os_name or "win8" in os_name:
        return "Windows 8"

    elif "win7" in os_name or "windows 7" in os_name:
        return "Windows 7"

    elif "linux" in os_name:
        return "Linux"

    elif "mac" in os_name or "os x" in os_name:
        return "macOS"

    elif "chrome" in os_name:
        return "Chrome OS"

    elif "unknown" in os_name:
        return "Unknown"

    else:
        return os_name.title()


df["Operating_System"] = df[
    "Operating_System"
].apply(
    standardize_os
)


# ============================================================
# 16. RATING
# ============================================================

df["Rating"] = pd.to_numeric(
    df["Rating"],
    errors="coerce"
)

# The source reports 0 for all ratings.
# Zero is treated as unavailable.

df.loc[
    df["Rating"] == 0,
    "Rating"
] = np.nan


# ============================================================
# 17. REVIEW COUNT
# ============================================================

df["Review_Count"] = pd.to_numeric(
    df["Review_Count"],
    errors="coerce"
)


# ============================================================
# 18. UNAVAILABLE SPECIFICATIONS
# ============================================================

# The source does not provide these fields.
# Do NOT invent values.

df["Resolution"] = np.nan

df["Weight_KG"] = np.nan


# ============================================================
# 19. CREATE PRICE CATEGORY
# ============================================================

def price_category(price):

    if pd.isna(price):
        return "Unknown"

    elif price < 500:
        return "Budget"

    elif price < 1000:
        return "Mid-Range"

    elif price < 1500:
        return "Premium"

    else:
        return "High-End"


df["Price_Category"] = df[
    "Price"
].apply(
    price_category
)


# ============================================================
# 20. CREATE RAM CATEGORY
# ============================================================

def ram_category(ram):

    if pd.isna(ram):
        return "Unknown"

    elif ram <= 4:
        return "4 GB or Less"

    elif ram <= 8:
        return "5-8 GB"

    elif ram <= 16:
        return "9-16 GB"

    else:
        return "More than 16 GB"


df["RAM_Category"] = df[
    "RAM_GB"
].apply(
    ram_category
)


# ============================================================
# 21. CHECK INVALID VALUES
# ============================================================

print("\n========== DATA QUALITY CHECK ==========")

print(
    "\nInvalid / missing prices:",
    df["Price"].isna().sum()
)

print(
    "Invalid / missing RAM:",
    df["RAM_GB"].isna().sum()
)

print(
    "Invalid / missing screen size:",
    df["Screen_Size_Inches"].isna().sum()
)


# ============================================================
# 22. REMOVE ROWS WITH MISSING ESSENTIAL VALUES
# ============================================================

# Price, Model and RAM are essential for our analysis.

before_rows = len(df)

df = df.dropna(
    subset=[
        "Model",
        "Price",
        "RAM_GB"
    ]
).copy()

after_rows = len(df)

print(
    "\nRows removed because of missing essential data:",
    before_rows - after_rows
)


# ============================================================
# 23. FINAL COLUMN ORDER
# ============================================================

df = df[
    [
        "Brand",
        "Model",
        "Price",
        "Price_Category",
        "CPU",
        "CPU_Family",
        "RAM_GB",
        "RAM_Category",
        "Storage",
        "Storage_Type",
        "GPU",
        "GPU_Type",
        "Screen_Size_Inches",
        "Resolution",
        "Operating_System",
        "Weight_KG",
        "Rating",
        "Review_Count",
        "Description"
    ]
]


# ============================================================
# 24. FINAL DATASET INFORMATION
# ============================================================

print("\n========== FINAL CLEANED DATA ==========")

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)

print("\nBrands:")
print(
    df["Brand"].value_counts()
)

print("\nCPU Families:")
print(
    df["CPU_Family"].value_counts()
)

print("\nStorage Types:")
print(
    df["Storage_Type"].value_counts()
)

print("\nGPU Types:")
print(
    df["GPU_Type"].value_counts()
)

print("\nRAM Categories:")
print(
    df["RAM_Category"].value_counts()
)

print("\nPrice Categories:")
print(
    df["Price_Category"].value_counts()
)


# ============================================================
# 25. SHOW FIRST 10 ROWS
# ============================================================

print("\n========== FIRST 10 CLEANED ROWS ==========")

print(
    df.head(10).to_string()
)


# ============================================================
# 26. SAVE FINAL CLEANED DATASET
# ============================================================

df.to_csv(
    "laptop_cleaned_data.csv",
    index=False
)


# ============================================================
# 27. FINAL MESSAGE
# ============================================================

print("\n==========================================")
print("FINAL DATA CLEANING COMPLETED")
print("==========================================")

print(
    "Original rows:",
    117
)

print(
    "Final cleaned rows:",
    len(df)
)

print(
    "Final columns:",
    len(df.columns)
)

print(
    "\nSaved file:"
)

print(
    "laptop_cleaned_data.csv"
)

print(
    "\nRaw file remains unchanged:"
)

print(
    "laptop_raw_data.csv"
)