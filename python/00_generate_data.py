import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

# -----------------------------
# Fake Netflix-style data
# -----------------------------
np.random.seed(42)

rows = 10000

plans = ["Basic", "Standard", "Premium"]
devices = ["Mobile", "Desktop", "Tablet", "TV"]
regions = ["North America", "Europe", "Asia", "South America"]

df = pd.DataFrame({
    "user_id": range(1, rows + 1),
    "subscription_plan": np.random.choice(plans, rows),
    "device": np.random.choice(devices, rows),
    "region": np.random.choice(regions, rows),
    "watch_minutes": np.random.normal(120, 40, rows).clip(10),
    "login_frequency": np.random.normal(15, 5, rows).clip(1),
    "days_inactive": np.random.normal(10, 7, rows).clip(0),
    "support_tickets": np.random.randint(0, 5, rows),
    "tenure_months": np.random.randint(1, 36, rows)
})

# Churn probability
df["churn_probability"] = (
    (df["days_inactive"] * 0.03)
    + (df["support_tickets"] * 0.05)
    - (df["watch_minutes"] * 0.001)
).clip(0, 1)

df["churn"] = np.where(df["churn_probability"] > 0.5, 1, 0)

# Save CSV
output_file = DATA / "subscriber_churn_dataset.csv"
df.to_csv(output_file, index=False)

print("✅ Dataset created:", output_file)
print(df.head())
