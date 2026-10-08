
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "customer_sales_raw.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True) 

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("TASK 1: DATA CLEANING & PREPROCESSING")
print("=" * 70)

print("\n1. DATASET SHAPE")
print(df.shape)

print("\n2. DATASET INFO")
print(df.info())

print("\n3. FIRST 5 ROWS")
print(df.head())

print("\n4. MISSING VALUES")
print(df.isnull().sum())

print("\n5. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

print("\n6. UNIQUE LOCATION VALUES BEFORE CLEANING")
print(sorted(df["Location"].dropna().astype(str).unique()))

print("\n7. UNIQUE GENDER VALUES BEFORE CLEANING")
print(sorted(df["Gender"].dropna().astype(str).unique()))

# Convert numeric columns safely.
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Purchase_Amount"] = pd.to_numeric(df["Purchase_Amount"], errors="coerce")

# Convert dates. First parse normal ISO dates, then fall back to day-first for values such as 18/01/2026.
df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"], errors="coerce")
missing_date = df["Purchase_Date"].isna()
df.loc[missing_date, "Purchase_Date"] = pd.to_datetime(
    df.loc[missing_date, "Purchase_Date"], dayfirst=True, errors="coerce"
)

# Fill missing numeric values with the median.
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Purchase_Amount"] = df["Purchase_Amount"].fillna(
    df["Purchase_Amount"].median()
)

# Standardize text fields.
df["Name"] = df["Name"].astype("string").str.strip().str.title()
df["Location"] = df["Location"].astype("string").str.strip().str.title()

df["Gender"] = (
    df["Gender"]
    .astype("string")
    .str.strip()
    .str.title()
    .replace({"Male": "M", "Female": "F"})
)

# Remove exact duplicate records.
df = df.drop_duplicates().reset_index(drop=True)

# Add a useful analysis column.
df["Month"] = df["Purchase_Date"].dt.to_period("M").astype(str)

print("\n8. AFTER CLEANING")
print("Shape:", df.shape)
print("\nMissing values after cleaning:")
print(df.isnull().sum())
print("\nDuplicate rows after cleaning:", df.duplicated().sum())
print("\nData types after cleaning:")
print(df.dtypes)

clean_file = OUTPUT_DIR / "customer_sales_cleaned.csv"
df.to_csv(clean_file, index=False)

print(f"\nCleaned dataset saved to: {clean_file}")
print("\nCleaned data:")
print(df.head(10).to_string(index=False))
