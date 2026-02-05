# ==========================================
# Phase 2 — Stock + Sector Analysis
# ==========================================

import pandas as pd
import os

print("Starting analysis...")

# ------------------------------------------
# Load stock data
# ------------------------------------------
df = pd.read_csv("csv/all_stocks.csv")

print("Rows loaded:", len(df))


# ------------------------------------------
# Load sector mapping
# ------------------------------------------
sector_df = pd.read_csv("csv/sector_data.csv")

print("Sector rows:", len(sector_df))


# ------------------------------------------
# Merge stock + sector
# ------------------------------------------
df = df.merge(sector_df, on="Ticker", how="left")


# ------------------------------------------
# Cleaning
# ------------------------------------------
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Ticker', 'date'])


# ------------------------------------------
# Daily return (stock level)
# ------------------------------------------
df['daily_return'] = df.groupby('Ticker')['close'].pct_change()


# ------------------------------------------
# Yearly return (stock level)
# ------------------------------------------
first_price = df.groupby('Ticker')['close'].first()
last_price = df.groupby('Ticker')['close'].last()

yearly_return = ((last_price - first_price) / first_price) * 100

print("\nTop 10 Gainers")
print(yearly_return.sort_values(ascending=False).head(10))


print("\nTop 10 Losers")
print(yearly_return.sort_values().head(10))


# ------------------------------------------
# Volatility (stock level)
# ------------------------------------------
volatility = df.groupby('Ticker')['daily_return'].std()

print("\nMost Volatile Stocks")
print(volatility.sort_values(ascending=False).head(10))


# ------------------------------------------
# Sector Analysis (NEW REQUIREMENT)
# ------------------------------------------

sector_return = df.groupby('Sector')['daily_return'].mean() * 100
sector_volatility = df.groupby('Sector')['daily_return'].std()

print("\nSector Average Return (%)")
print(sector_return.sort_values(ascending=False))

print("\nSector Volatility")
print(sector_volatility.sort_values(ascending=False))


# ------------------------------------------
# Save combined final dataset
# ------------------------------------------
os.makedirs("csv", exist_ok=True)
df.to_csv("csv/final_data.csv", index=False)


# ------------------------------------------
# Save sector summary file
# ------------------------------------------
sector_summary = pd.DataFrame({
    "Avg_Return_%": sector_return,
    "Volatility": sector_volatility
})

sector_summary.to_csv("csv/sector_summary.csv")


# ------------------------------------------
# Create separate ticker files
# ------------------------------------------
os.makedirs("csv/tickers", exist_ok=True)

for ticker, group in df.groupby('Ticker'):
    group.to_csv(f"csv/tickers/{ticker}.csv", index=False)


print("\nAnalysis complete")
