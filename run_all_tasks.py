from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

tasks = [
    ("Task 1", ROOT / "Task_1_Data_Cleaning" / "task1_data_cleaning.py"),
    ("Task 2", ROOT / "Task_2_EDA" / "task2_eda.py"),
    ("Task 3", ROOT / "Task_3_Data_Visualization" / "task3_visualization.py"),
    ("Task 4", ROOT / "Task_4_Customer_Data_Analysis" / "task4_customer_analysis.py"),
    ("Task 5", ROOT / "Task_5_Web_Data_Extraction" / "task5_web_scraping.py"),
]

for name, script in tasks:
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)
    result = subprocess.run([sys.executable, str(script)])
    if result.returncode != 0:
        print(f"{name} failed with exit code {result.returncode}.")
        sys.exit(result.returncode)

print("\nAll tasks completed successfully.")
