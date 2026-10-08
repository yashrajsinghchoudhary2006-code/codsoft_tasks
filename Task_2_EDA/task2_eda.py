 
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "customer_sales_clean.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE, parse_dates=["Purchase_Date"])

print("=" * 70)
print("TASK 2: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# 1. Basic descriptive statistics
numeric_cols = ["Age", "Purchase_Amount"]
print("\nDESCRIPTIVE STATISTICS")
print(df[numeric_cols].describe())

# 2. Distribution/trends
category_sales = df.groupby("Category")["Purchase_Amount"].agg(["count", "sum", "mean"])
location_sales = df.groupby("Location")["Purchase_Amount"].agg(["count", "sum", "mean"])
gender_sales = df.groupby("Gender")["Purchase_Amount"].agg(["count", "sum", "mean"])
monthly_sales = df.groupby("Month")["Purchase_Amount"].sum()

print("\nSALES BY CATEGORY")
print(category_sales.sort_values("sum", ascending=False))

print("\nSALES BY LOCATION")
print(location_sales.sort_values("sum", ascending=False))

print("\nSALES BY GENDER")
print(gender_sales)

print("\nMONTHLY SALES")
print(monthly_sales)

# 3. Relationship between age and purchase amount
print("\nCORRELATION: AGE vs PURCHASE AMOUNT")
print(df["Age"].corr(df["Purchase_Amount"]))

# 4. Outlier detection using IQR
q1 = df["Purchase_Amount"].quantile(0.25)
q3 = df["Purchase_Amount"].quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[
    (df["Purchase_Amount"] < lower) |
    (df["Purchase_Amount"] > upper)
]

print("\nOUTLIER LIMITS")
print("Lower:", lower)
print("Upper:", upper)
print("Number of outliers:", len(outliers))
print(outliers[["Customer_ID", "Name", "Purchase_Amount", "Category"]])

# 5. Visual analysis

plt.figure(figsize=(8, 5))
plt.hist(df["Purchase_Amount"], bins=8, edgecolor="black")
plt.title("Distribution of Purchase Amount")
plt.xlabel("Purchase Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "purchase_distribution.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
box_data = [df.loc[df["Category"] == cat, "Purchase_Amount"] for cat in df["Category"].dropna().unique()]
box_labels = list(df["Category"].dropna().unique())
plt.boxplot(box_data, labels=box_labels)
plt.title("Purchase Amount by Category")
plt.xlabel("Category")
plt.ylabel("Purchase Amount")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_boxplot.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
for gender, group in df.groupby("Gender"):
    plt.scatter(group["Age"], group["Purchase_Amount"], label=gender, s=60)
plt.title("Age vs Purchase Amount")
plt.xlabel("Age")
plt.ylabel("Purchase Amount")
plt.legend(title="Gender")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "age_vs_purchase.png", dpi=150)
plt.close()

# 6. Business questions
top_customer = df.loc[df["Purchase_Amount"].idxmax()]
top_category = category_sales["sum"].idxmax()
top_location = location_sales["sum"].idxmax()
avg_purchase = df["Purchase_Amount"].mean()

report = f"""
CODSOFT TASK 2 - EDA REPORT

Dataset rows: {len(df)}
Average purchase amount: {avg_purchase:.2f}
Highest-value customer in this sample: {top_customer['Name']} (amount={top_customer['Purchase_Amount']:.2f})
Category with highest total sales: {top_category}
Location with highest total sales: {top_location}
Age/Purchase correlation: {df['Age'].corr(df['Purchase_Amount']):.3f}
Detected purchase-amount outliers using IQR: {len(outliers)}

Key observations:
1. Category totals show how sales are distributed across product categories.
2. Location totals show where sample sales are concentrated.
3. The histogram shows the purchase amount distribution.
4. The boxplot helps compare spread and outliers across categories.
5. The scatter plot helps inspect the relationship between customer age and purchase amount.
"""

(OUTPUT_DIR / "eda_report.txt").write_text(report.strip(), encoding="utf-8")
print("\nEDA report and charts saved in:", OUTPUT_DIR)
