 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "customer_sales_clean.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE, parse_dates=["Purchase_Date"])

# Customer segments based on purchasing behavior.
# Thresholds are simple and editable for academic/demo use.
def segment_customer(row):
    if row["Purchase_Amount"] >= 2500:
        return "High Value"
    elif row["Purchase_Amount"] >= 1200:
        return "Medium Value"
    return "Low Value"

df["Segment"] = df.apply(segment_customer, axis=1)

# Age groups
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 45, 100],
    labels=["<=25", "26-35", "36-45", "46+"],
    include_lowest=True
)

print("=" * 70)
print("TASK 4: CUSTOMER DATA ANALYSIS")
print("=" * 70)

print("\nCUSTOMER SEGMENTS")
print(df["Segment"].value_counts())

segment_summary = df.groupby("Segment", observed=False)["Purchase_Amount"].agg(
    Customers="count",
    Total_Spending="sum",
    Average_Spending="mean"
).sort_values("Total_Spending", ascending=False)

print("\nSEGMENT SUMMARY")
print(segment_summary)

print("\nAGE GROUP SUMMARY")
age_summary = df.groupby("Age_Group", observed=False)["Purchase_Amount"].agg(
    Customers="count",
    Total_Spending="sum",
    Average_Spending="mean"
)
print(age_summary)

print("\nLOCATION SUMMARY")
location_summary = df.groupby("Location")["Purchase_Amount"].agg(
    Customers="count",
    Total_Spending="sum",
    Average_Spending="mean"
).sort_values("Total_Spending", ascending=False)
print(location_summary)

# Most valuable sample customers
top_customers = df.nlargest(5, "Purchase_Amount")[
    ["Customer_ID", "Name", "Age", "Location", "Category", "Purchase_Amount", "Segment"]
]
print("\nTOP 5 CUSTOMERS BY PURCHASE AMOUNT")
print(top_customers.to_string(index=False))

# Visual 1: segment bar chart
plt.figure(figsize=(8, 5))
segment_summary["Total_Spending"].plot(kind="bar")
plt.title("Total Spending by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Spending")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_segment_spending.png", dpi=150)
plt.close()

# Visual 2: location x segment
pivot = pd.pivot_table(
    df,
    index="Location",
    columns="Segment",
    values="Purchase_Amount",
    aggfunc="sum",
    fill_value=0,
    observed=False
)
plt.figure(figsize=(9, 5))
pivot.plot(kind="bar", figsize=(9, 5))
plt.title("Customer Spending by Location and Segment")
plt.xlabel("Location")
plt.ylabel("Total Spending")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_location_segment.png", dpi=150)
plt.close()

# Simple marketing suggestions based on data patterns.
high_value_share = (df["Segment"] == "High Value").mean() * 100
top_segment = segment_summary.index[0]
top_location = location_summary.index[0]

suggestions = f"""
CUSTOMER ANALYSIS REPORT

High-value customer share in this sample: {high_value_share:.1f}%
Segment contributing the most total spending: {top_segment}
Location contributing the most total spending: {top_location}

Suggested actions:
1. Offer loyalty rewards or early-access benefits to High Value customers.
2. Use targeted offers to move Medium Value customers toward higher purchase levels.
3. Test smaller introductory discounts or bundles for Low Value customers.
4. Create location-specific campaigns for the locations with stronger sales.
"""

(OUTPUT_DIR / "customer_analysis_report.txt").write_text(
    suggestions.strip(), encoding="utf-8"
)

df.to_csv(OUTPUT_DIR / "customer_segments.csv", index=False)

print("\nReports, segmented data, and charts saved in:", OUTPUT_DIR)
