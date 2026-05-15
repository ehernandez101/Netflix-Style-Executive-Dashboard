import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

df = pd.read_csv(DATA / "subscriber_churn_dataset.csv")

total_subscribers = len(df)
churn_rate = df["churn"].mean()
retention_rate = 1 - churn_rate
avg_watch_minutes = df["watch_minutes"].mean()
avg_inactive_days = df["days_inactive"].mean()

print("===== NETFLIX-STYLE KPI SUMMARY =====")
print(f"Total Subscribers: {total_subscribers:,}")
print(f"Churn Rate: {churn_rate:.2%}")
print(f"Retention Rate: {retention_rate:.2%}")
print(f"Avg Watch Minutes: {avg_watch_minutes:.1f}")
print(f"Avg Days Inactive: {avg_inactive_days:.1f}")

print("\n===== CHURN BY PLAN =====")
print(df.groupby("subscription_plan")["churn"].mean().sort_values(ascending=False))

print("\n===== CHURN BY DEVICE =====")
print(df.groupby("device")["churn"].mean().sort_values(ascending=False))

print("\n===== CHURN BY REGION =====")
print(df.groupby("region")["churn"].mean().sort_values(ascending=False))
