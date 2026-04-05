import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

OUTPUT_DIR = "/Users/mahitpatel/Documents/Hospital_Readmissions_Project/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_PATH = "/Users/mahitpatel/Documents/Hospital_Readmissions_Project/readmissions.csv"

df = pd.read_csv(DATA_PATH)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head(3))

# Clean
df = df.dropna(subset=["Excess Readmission Ratio"])
df["Number of Discharges"] = pd.to_numeric(df["Number of Discharges"], errors="coerce")
df["Penalized"] = df["Excess Readmission Ratio"] > 1.0

MEASURE_LABELS = {
    "READM-30-HIP-KNEE-HRRP": "Hip/Knee Replacement",
    "READM-30-CABG-HRRP":     "Heart Bypass (CABG)",
    "READM-30-AMI-HRRP":      "Heart Attack (AMI)",
    "READM-30-COPD-HRRP":     "COPD",
    "READM-30-PN-HRRP":       "Pneumonia",
    "READM-30-HF-HRRP":       "Heart Failure",
}
df["Condition"] = df["Measure Name"].map(MEASURE_LABELS)

print(f"Clean rows : {len(df):,}")
print(f"Hospitals  : {df['Facility ID'].nunique():,}")
print(f"States     : {df['State'].nunique()}")
print(f"Penalized %: {df['Penalized'].mean()*100:.1f}%")

# Analysis 1 — Avg ERR by condition
err_by_condition = (
    df.groupby("Condition")["Excess Readmission Ratio"]
    .mean().sort_values(ascending=False).reset_index()
)
err_by_condition.columns = ["Condition", "Avg_ERR"]
print("=== AVG ERR BY CONDITION ===")
print(err_by_condition.to_string(index=False))

# Analysis 2 — Penalty rate by state
state_stats = (
    df.groupby("State")
    .agg(Total=("Penalized","count"),
         Penalized_Count=("Penalized","sum"),
         Avg_ERR=("Excess Readmission Ratio","mean"))
    .reset_index()
)
state_stats["Pct_Penalized"] = (
    state_stats["Penalized_Count"] / state_stats["Total"] * 100
).round(1)
state_stats = state_stats.sort_values("Pct_Penalized", ascending=False)
print("\n=== TOP 10 STATES BY PENALTY RATE ===")
print(state_stats.head(10).to_string(index=False))

# Analysis 3 — Top 15 worst hospitals
hosp_stats = (
    df.groupby(["Facility Name","State"])
    .agg(Avg_ERR=("Excess Readmission Ratio","mean"),
         Conditions_Reported=("Condition","count"))
    .reset_index()
)
top_hospitals = (
    hosp_stats[hosp_stats["Conditions_Reported"] >= 3]
    .sort_values("Avg_ERR", ascending=False)
    .head(15)
)
print("\n=== TOP 15 HIGHEST RISK HOSPITALS ===")
print(top_hospitals.to_string(index=False))

# Chart 1 — Avg ERR by Condition
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#D7191C" if v > 1 else "#2C7BB6" for v in err_by_condition["Avg_ERR"]]
bars = ax.barh(err_by_condition["Condition"], err_by_condition["Avg_ERR"],
               color=colors, edgecolor="white", height=0.6)
ax.axvline(1.0, color="black", linewidth=1.3, linestyle="--", label="Benchmark (ERR = 1.0)")
ax.set_xlabel("Average Excess Readmission Ratio")
ax.set_title("Average Excess Readmission Ratio by Condition\n"
             "(ERR > 1.0 = more readmissions than expected → penalty risk)", fontsize=12)
ax.legend()
for bar, val in zip(bars, err_by_condition["Avg_ERR"]):
    ax.text(val + 0.001, bar.get_y() + bar.get_height()/2,
            f"{val:.4f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart1_err_by_condition.png", dpi=150)
plt.close()
print("Saved chart 1")

# Chart 2 — Top 20 States by % Penalized
top20 = state_stats.head(20)
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(top20["State"][::-1], top20["Pct_Penalized"][::-1],
        color="#D7191C", edgecolor="white", height=0.6)
ax.set_xlabel("% of Hospital-Condition Pairs Exceeding Benchmark")
ax.set_title("Top 20 States by Readmission Penalty Rate", fontsize=12)
ax.xaxis.set_major_formatter(mticker.PercentFormatter())
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart2_top_states_penalized.png", dpi=150)
plt.close()
print("Saved chart 2")

# Chart 3 — Box plot by condition
fig, ax = plt.subplots(figsize=(11, 6))
order = err_by_condition["Condition"].tolist()
box_data = [df[df["Condition"] == c]["Excess Readmission Ratio"].dropna().values
            for c in order]
bp = ax.boxplot(box_data, labels=order, patch_artist=True,
                flierprops=dict(marker="o", markersize=2, alpha=0.4),
                medianprops=dict(color="black", linewidth=1.5))
blues = ["#084594","#2171b5","#4292c6","#6baed6","#9ecae1","#c6dbef"]
for patch, color in zip(bp["boxes"], blues):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
ax.axhline(1.0, color="red", linewidth=1.3, linestyle="--", label="Benchmark (ERR = 1.0)")
ax.set_ylabel("Excess Readmission Ratio")
ax.set_title("Spread of Hospital Performance by Condition\n"
             "(Boxes show middle 50% of hospitals; dots = outliers)", fontsize=12)
ax.tick_params(axis="x", rotation=18)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart3_err_distribution.png", dpi=150)
plt.close()
print("Saved chart 3")

# Chart 4 — Top 15 Worst Hospitals
fig, ax = plt.subplots(figsize=(11, 6))
labels = (top_hospitals["Facility Name"].str.title()
          + " (" + top_hospitals["State"] + ")")
ax.barh(labels[::-1], top_hospitals["Avg_ERR"][::-1],
        color="#D7191C", edgecolor="white", height=0.6)
ax.axvline(1.0, color="black", linewidth=1.3, linestyle="--", label="Benchmark")
ax.set_xlabel("Average Excess Readmission Ratio")
ax.set_title("Top 15 Highest-Risk Hospitals\n"
             "(Avg ERR across all reported conditions, min 3 conditions)", fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart4_worst_hospitals.png", dpi=150)
plt.close()
print("Saved chart 4")

# Export clean CSV for Tableau
tableau_df = df[[
    "Facility Name","Facility ID","State","Condition",
    "Number of Discharges","Excess Readmission Ratio",
    "Predicted Readmission Rate","Expected Readmission Rate",
    "Number of Readmissions","Penalized"
]].copy()
tableau_df["Number of Readmissions"] = pd.to_numeric(
    tableau_df["Number of Readmissions"], errors="coerce"
)
tableau_df.to_csv(f"{OUTPUT_DIR}/readmissions_clean_tableau.csv", index=False)
print("Saved Tableau CSV")
print(f"\nAll done! Files in: {OUTPUT_DIR}")