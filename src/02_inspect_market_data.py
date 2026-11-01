
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==============================================
# 1. LOCATE THE PROJECT AND ORIGINAL WORKBOOK
# ==============================================

ROOT = Path(__file__).resolve().parents[1]

file_path = ROOT / "data" / "raw" / "smd_hourly_converted.xlsx"

processed_dir = ROOT / "data" / "processed"
figure_dir = ROOT / "results" / "figures"
table_dir = ROOT / "results" / "tables"

processed_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)
table_dir.mkdir(parents=True, exist_ok=True)

if not file_path.exists():
    raise FileNotFoundError(f"Workbook not found: {file_path}")


# ==============================================
# 2. INSPECT THE WORKBOOK
# ==============================================

excel_file = pd.ExcelFile(file_path, engine="openpyxl")

print("WORKSHEETS:")
print(excel_file.sheet_names)

# Extract only Southeast Massachusetts.
df = pd.read_excel(
    excel_file,
    sheet_name="SEMASS"
)

print("\nDATASET DIMENSIONS:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST FIVE ROWS:")
print(df.head())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nMISSING VALUES:")
print(df.isna().sum())


# ==============================================
# 3. PREPARE THE REQUIRED COLUMNS
# ==============================================

df.columns = [str(c).strip() for c in df.columns]

required = ["Date", "Hour", "DA_LMP"]

if not all(c in df.columns for c in required):
    raise ValueError("Required columns are missing.")

df = df[required].copy()

# Handle either Excel date serials or parsed dates.
if pd.api.types.is_numeric_dtype(df["Date"]):
    df["Date"] = pd.to_datetime(
        df["Date"],
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )
else:
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

df["Date"] = df["Date"].dt.normalize()

df["Hour"] = pd.to_numeric(
    df["Hour"], errors="coerce"
)

df["DA_LMP"] = pd.to_numeric(
    df["DA_LMP"], errors="coerce"
)

if df[required].isna().any().any():
    raise ValueError(
        "Invalid or missing values detected. "
        "Investigate before continuing."
    )

# Sort by date and hour-ending value.
df = df.sort_values(
    ["Date", "Hour"]
).reset_index(drop=True)


# ==============================================
# 4. CHECK DATA QUALITY
# ==============================================

duplicate_keys = df.duplicated(
    subset=["Date", "Hour"]
).sum()

hours_per_day = df.groupby("Date")["Hour"].agg(
    ["count", "nunique", "min", "max"]
)

valid_days = (
    (hours_per_day["count"] == 24)
    & (hours_per_day["nunique"] == 24)
    & (hours_per_day["min"] == 1)
    & (hours_per_day["max"] == 24)
).sum()

negative_count = (df["DA_LMP"] < 0).sum()
zero_count = (df["DA_LMP"] == 0).sum()

print("\nDATA QUALITY REPORT")
print("Total observations:", len(df))
print("Unique dates:", df["Date"].nunique())
print("Duplicate date-hour keys:", duplicate_keys)
print("Days with all 24 distinct hour-ending values:",
      valid_days)
print("Missing DA-LMP values:", df["DA_LMP"].isna().sum())
print("Negative prices:", negative_count)
print("Zero prices:", zero_count)


# ==============================================
# 5. CALCULATE PRICE STATISTICS
# ==============================================

print("\nPRICE STATISTICS ($/MWh):")

print(df["DA_LMP"].describe())

summary = pd.DataFrame({
    "Metric": [
        "Observations",
        "Start date",
        "End date",
        "Mean price",
        "Median price",
        "Standard deviation",
        "Minimum price",
        "Maximum price",
        "Negative-price observations",
        "Zero-price observations",
        "Duplicate date-hour keys",
    ],

    "Value": [
        len(df),
        str(df["Date"].min().date()),
        str(df["Date"].max().date()),
        df["DA_LMP"].mean(),
        df["DA_LMP"].median(),
        df["DA_LMP"].std(),
        df["DA_LMP"].min(),
        df["DA_LMP"].max(),
        negative_count,
        zero_count,
        duplicate_keys,
    ]
})

summary.to_csv(
    table_dir / "market_data_audit.csv",
    index=False
)


# ==============================================
# 6. SAVE THE EXTRACTED PRICE DATA
# ==============================================

output = df.copy()

output["Date"] = output["Date"].dt.strftime("%Y-%m-%d")

output.to_csv(
    processed_dir / "semass_2015_da_prices.csv",
    index=False
)


# Save unusual price observations for investigation.
flags = df[df["DA_LMP"] <= 0].copy()

flags["Price_flag"] = flags["DA_LMP"].apply(
    lambda x: "Negative" if x < 0 else "Zero"
)

flags.to_csv(
    table_dir / "price_observations_to_investigate.csv",
    index=False
)


# ==============================================
# 7. PREPARE THE HOURLY TIME AXIS
# ==============================================

# Hour is recorded as hour-ending, not hour-beginning.
df["Hour_ending_time"] = (
    df["Date"] + pd.to_timedelta(df["Hour"], unit="h")
)


# ==============================================
# 8. FULL-YEAR PRICE PLOT
# ==============================================

fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    df["Hour_ending_time"],
    df["DA_LMP"],
    linewidth=0.45
)

ax.set_title("2015 SEMASS Day-Ahead LMP")
ax.set_xlabel("Hour-ending date/time (market convention)")
ax.set_ylabel("Price ($/MWh)")
ax.grid(True, alpha=0.3)

fig.tight_layout()

fig.savefig(
    figure_dir / "semass_2015_annual_prices.png",
    dpi=200
)

plt.close(fig)


# ==============================================
# 9. JULY PRICE INVESTIGATION
# ==============================================

july = df[
    (df["Date"] >= "2015-07-01")
    & (df["Date"] < "2015-07-08")
]

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    july["Hour_ending_time"],
    july["DA_LMP"],
    marker=".",
    markersize=3
)

ax.axhline(0, linestyle="--", linewidth=1)

ax.set_title("SEMASS Day-Ahead Prices: 1–7 July 2015")
ax.set_xlabel("Hour-ending date/time")
ax.set_ylabel("Price ($/MWh)")
ax.grid(True, alpha=0.3)

fig.tight_layout()

fig.savefig(
    figure_dir / "semass_july_price_analysis.png",
    dpi=200
)

plt.close(fig)


# ==============================================
# 10. PRICE DISTRIBUTION
# ==============================================

fig, ax = plt.subplots(figsize=(9, 5))

ax.hist(
    df["DA_LMP"],
    bins=50
)

ax.set_title("2015 SEMASS Day-Ahead Price Distribution")
ax.set_xlabel("Price ($/MWh)")
ax.set_ylabel("Number of hourly observations")
ax.grid(True, alpha=0.3)

fig.tight_layout()

fig.savefig(
    figure_dir / "semass_price_distribution.png",
    dpi=200
)

plt.close(fig)


# ==============================================
# 11. MONTHLY PRICE SUMMARY
# ==============================================

monthly = (
    df.groupby(df["Date"].dt.month)["DA_LMP"]
    .agg(["count", "mean", "median", "min", "max"])
)

monthly.index.name = "Month"

monthly.to_csv(
    table_dir / "monthly_price_summary.csv"
)

print("\nMONTHLY PRICE SUMMARY:")
print(monthly.round(3))

print("\nANALYSIS COMPLETE.")
