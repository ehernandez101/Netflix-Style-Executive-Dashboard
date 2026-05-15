import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VISUALS = ROOT / "visuals"
VISUALS.mkdir(exist_ok=True)

df = pd.read_csv(DATA / "subscriber_churn_dataset.csv")

BG = "#0B0F19"
CARD = "#111827"
TEXT = "#F9FAFB"
RED = "#E50914"
BLUE = "#38BDF8"
GREEN = "#22C55E"
PURPLE = "#A78BFA"

def style_chart(title, xlabel, ylabel):
    fig = plt.gcf()
    ax = plt.gca()

    fig.set_facecolor(BG)
    ax.set_facecolor(CARD)

    ax.set_title(title, color=TEXT, fontsize=16, fontweight="bold", pad=14)
    ax.set_xlabel(xlabel, color=TEXT, fontsize=11)
    ax.set_ylabel(ylabel, color=TEXT, fontsize=11)
    ax.tick_params(colors=TEXT)

    for spine in ax.spines.values():
        spine.set_color("#334155")

    ax.grid(axis="y", alpha=0.25)

# Churn by Plan
churn_by_plan = df.groupby("subscription_plan")["churn"].mean().reset_index()

plt.figure(figsize=(9, 5))
plt.bar(churn_by_plan["subscription_plan"], churn_by_plan["churn"], color=RED)
style_chart("Churn Rate by Subscription Plan", "Subscription Plan", "Churn Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(VISUALS / "churn_by_plan.png", dpi=180)
plt.close()

# Churn by Device
churn_by_device = df.groupby("device")["churn"].mean().reset_index()

plt.figure(figsize=(9, 5))
plt.bar(churn_by_device["device"], churn_by_device["churn"], color=BLUE)
style_chart("Churn Rate by Device", "Device", "Churn Rate")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(VISUALS / "churn_by_device.png", dpi=180)
plt.close()

# Churn by Region
churn_by_region = df.groupby("region")["churn"].mean().reset_index()

plt.figure(figsize=(9, 5))
plt.bar(churn_by_region["region"], churn_by_region["churn"], color=GREEN)
style_chart("Churn Rate by Region", "Region", "Churn Rate")
plt.xticks(rotation=25)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(VISUALS / "churn_by_region.png", dpi=180)
plt.close()

# Watch Minutes: Retained vs Churned
watch_by_churn = df.groupby("churn")["watch_minutes"].mean().reset_index()
watch_by_churn["status"] = watch_by_churn["churn"].map({0: "Retained", 1: "Churned"})

plt.figure(figsize=(9, 5))
plt.bar(watch_by_churn["status"], watch_by_churn["watch_minutes"], color=[GREEN, RED])
style_chart("Avg Watch Minutes: Retained vs Churned", "Subscriber Status", "Avg Watch Minutes")
plt.tight_layout()
plt.savefig(VISUALS / "watch_minutes_retained_vs_churned.png", dpi=180)
plt.close()

# Subscription Plan Distribution
plan_counts = df["subscription_plan"].value_counts().reset_index()
plan_counts.columns = ["subscription_plan", "subscribers"]

plt.figure(figsize=(9, 5))
plt.bar(plan_counts["subscription_plan"], plan_counts["subscribers"], color=PURPLE)
style_chart("Subscription Plan Distribution", "Subscription Plan", "Subscribers")
plt.tight_layout()
plt.savefig(VISUALS / "subscription_plan_distribution.png", dpi=180)
plt.close()

print("✅ Netflix-style visuals created.")
