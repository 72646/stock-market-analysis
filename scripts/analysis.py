# =====================================================
# COMPLETE STOCK + SECTOR ANALYSIS PIPELINE
# FINAL STABLE VERSION (ALL REQUIREMENTS INCLUDED)
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt
import os


print("Starting full analysis pipeline...\n")


# =====================================================
# Create folders
# =====================================================

os.makedirs("csv", exist_ok=True)
os.makedirs("csv/tickers", exist_ok=True)
os.makedirs("csv/charts", exist_ok=True)


# =====================================================
# LOAD DATA
# =====================================================

print("Loading datasets...")

stock_path = "csv/all_stocks.csv"
sector_path = "csv/Sector_data.csv"

df = pd.read_csv(stock_path)
sector_df = pd.read_csv(sector_path)


# =====================================================
# CLEAN COLUMN NAMES (avoid hidden spaces issues)
# =====================================================

df.columns = df.columns.str.strip()
sector_df.columns = sector_df.columns.str.strip()

print("Stock columns :", list(df.columns))
print("Sector columns:", list(sector_df.columns))


# =====================================================
# FIX SECTOR FILE FORMAT
# Sector file format:
# COMPANY | sector | Symbol
# Symbol = "AXIS BANK: AXISBANK"
# We must extract ticker after ":"
# =====================================================

sector_df.rename(columns={"sector": "Sector"}, inplace=True)

sector_df["Ticker"] = (
    sector_df["Symbol"]
    .str.split(":")
    .str[-1]
    .str.strip()
)

sector_df = sector_df[["Ticker", "Sector"]]


# =====================================================
# MERGE STOCK + SECTOR
# =====================================================

print("\nMerging sector information...")

df = df.merge(sector_df, on="Ticker", how="left")


# =====================================================
# CLEAN + SORT
# =====================================================

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["Ticker", "date"])


# =====================================================
# DAILY RETURN
# Formula:
# (today - yesterday) / yesterday
# =====================================================

print("Calculating daily returns...")

df["daily_return"] = df.groupby("Ticker")["close"].pct_change()


# =====================================================
# YEARLY RETURN
# Formula:
# (last - first) / first * 100
# =====================================================

print("Calculating yearly returns...")

first_price = df.groupby("Ticker")["close"].first()
last_price = df.groupby("Ticker")["close"].last()

returns = ((last_price - first_price) / first_price) * 100

print("\nTop 10 Gainers")
print(returns.sort_values(ascending=False).head(10))

print("\nTop 10 Losers")
print(returns.sort_values().head(10))


# =====================================================
# VOLATILITY
# Standard deviation of daily returns
# =====================================================

print("\nCalculating volatility...")

volatility = df.groupby("Ticker")["daily_return"].std()

print("\nMost Volatile Stocks")
print(volatility.sort_values(ascending=False).head(10))


# =====================================================
# SECTOR ANALYSIS
# =====================================================

print("\nRunning sector analysis...")

sector_return = df.groupby("Sector")["daily_return"].mean() * 100
sector_volatility = df.groupby("Sector")["daily_return"].std()

sector_summary = pd.DataFrame({
    "Avg_Return_%": sector_return,
    "Volatility": sector_volatility
})

sector_summary.to_csv("csv/sector_summary.csv", index=True)


# =====================================================
# SAVE FINAL DATA
# =====================================================

print("\nSaving final dataset...")

df.to_csv("csv/final_data.csv", index=False)


# =====================================================
# CREATE ONE FILE PER TICKER
# =====================================================

print("Creating per-ticker CSV files...")

for ticker, group in df.groupby("Ticker"):
    group.to_csv(f"csv/tickers/{ticker}.csv", index=False)


# =====================================================
# CUMULATIVE RETURN CHART
# Formula: (1+r).cumprod()
# =====================================================

print("Generating cumulative return chart...")

top5 = returns.sort_values(ascending=False).head(5).index

plt.figure()

for ticker in top5:
    stock = df[df["Ticker"] == ticker].copy()
    stock["cum_return"] = (1 + stock["daily_return"]).cumprod()
    plt.plot(stock["date"], stock["cum_return"], label=ticker)

plt.legend()
plt.title("Top 5 Cumulative Return")
plt.tight_layout()
plt.savefig("csv/charts/cumulative_return.png")
plt.close()


# =====================================================
# SECTOR BAR CHART
# =====================================================

print("Generating sector chart...")

if not sector_return.empty:
    plt.figure()
    sector_return.sort_values(ascending=False).plot(kind="bar")
    plt.title("Sector Average Return (%)")
    plt.tight_layout()
    plt.savefig("csv/charts/sector_return.png")
    plt.close()


# =====================================================
# CORRELATION HEATMAP
# =====================================================

print("Generating correlation heatmap...")

pivot = df.pivot_table(index="date", columns="Ticker", values="close")
corr = pivot.corr()

plt.figure(figsize=(10, 8))
plt.imshow(corr, aspect="auto")
plt.colorbar()
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("csv/charts/correlation_heatmap.png")
plt.close()


# =====================================================
# MONTHLY TOP/BOTTOM ANALYSIS
# =====================================================

print("Generating monthly charts...")

df["month"] = df["date"].dt.month

monthly = (
    df.groupby(["month", "Ticker"])["daily_return"]
    .mean()
    .reset_index()
)

for m in range(1, 13):

    month_df = monthly[monthly["month"] == m]

    if month_df.empty:
        continue

    top5 = month_df.sort_values("daily_return", ascending=False).head(5)
    bottom5 = month_df.sort_values("daily_return").head(5)

    combined = pd.concat([top5, bottom5])

    plt.figure()
    plt.bar(combined["Ticker"], combined["daily_return"])
    plt.xticks(rotation=45)
    plt.title(f"Month {m} Top/Bottom Stocks")
    plt.tight_layout()
    plt.savefig(f"csv/charts/month_{m}.png")
    plt.close()


print("\nAnalysis pipeline completed successfully.")
