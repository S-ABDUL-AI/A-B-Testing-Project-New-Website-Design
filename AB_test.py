# ab_test_analysis.py
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# 1. Load the dataset
df = pd.read_csv("ab_test_data.csv")

# 2. Summarize group sizes and conversions
summary = df.groupby("group")["converted"].agg(["count", "sum", "mean"])
summary.rename(columns={"count": "Total Users", "sum": "Conversions", "mean": "Conversion Rate"}, inplace=True)
print("Summary of A/B Test Results:\n", summary, "\n")

# 3. Perform hypothesis test (Z-test for proportions)
conversions = summary["Conversions"].values
samples = summary["Total Users"].values

z_stat, p_val = proportions_ztest(count=conversions, nobs=samples)
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_val:.4f}")

if p_val < 0.05:
    print("✅ Statistically significant difference between groups (reject null hypothesis).")
else:
    print("❌ No statistically significant difference (fail to reject null hypothesis).")

# 4. Visualization
summary["Conversion Rate"].plot(kind="bar", color=["skyblue", "salmon"], rot=0)
plt.title("Conversion Rate by Group (A vs B)")
plt.ylabel("Conversion Rate")
plt.show()
