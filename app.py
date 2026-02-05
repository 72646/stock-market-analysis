import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Stock Market Analysis Dashboard")

# =====================================
# Load data
# =====================================

df = pd.read_csv("csv/final_data.csv")
df['date'] = pd.to_datetime(df['date'])


# =====================================
# Sidebar navigation
# =====================================

view = st.sidebar.selectbox(
    "Select View",
    [
        "Stock Analysis",
        "Sector Analysis",
        "Market Summary",
        "Correlation Heatmap",
        "Raw Data"
    ]
)


# =====================================
# 1️⃣ STOCK ANALYSIS VIEW
# =====================================

if view == "Stock Analysis":

    st.header("Stock Analysis")

    stocks = sorted(df['Ticker'].unique())
    ticker = st.sidebar.selectbox("Select Stock", stocks)

    stock_df = df[df['Ticker'] == ticker]

    col1, col2, col3 = st.columns(3)

    first = stock_df['close'].iloc[0]
    last = stock_df['close'].iloc[-1]

    total_return = ((last - first) / first) * 100
    volatility = stock_df['daily_return'].std()

    col1.metric("Start Price", round(first, 2))
    col2.metric("End Price", round(last, 2))
    col3.metric("Return %", round(total_return, 2))

    st.subheader("Price Chart")

    fig, ax = plt.subplots()
    ax.plot(stock_df['date'], stock_df['close'])
    st.pyplot(fig)

    st.subheader("Stock Table")
    st.dataframe(stock_df.tail(20))


# =====================================
# 2️⃣ SECTOR ANALYSIS VIEW
# =====================================

elif view == "Sector Analysis":

    st.header("Sector Analysis")

    sector_return = df.groupby('Sector')['daily_return'].mean() * 100

    st.subheader("Sector Returns Table")
    st.dataframe(sector_return.sort_values(ascending=False))

    st.subheader("Sector Chart")

    fig, ax = plt.subplots()
    sector_return.sort_values().plot(kind='bar', ax=ax)
    st.pyplot(fig)


# =====================================
# 3️⃣ MARKET SUMMARY VIEW
# =====================================

elif view == "Market Summary":

    st.header("Market Summary")

    avg_price = df['close'].mean()
    avg_volume = df['volume'].mean()

    green = (df.groupby('Ticker')['close'].last() >
             df.groupby('Ticker')['close'].first()).sum()

    red = (df.groupby('Ticker')['close'].last() <
           df.groupby('Ticker')['close'].first()).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Average Price", round(avg_price, 2))
    col2.metric("Average Volume", int(avg_volume))
    col3.metric("Green vs Red", f"{green} / {red}")

    st.subheader("Top Gainers")

    first = df.groupby('Ticker')['close'].first()
    last = df.groupby('Ticker')['close'].last()
    returns = ((last - first) / first) * 100

    st.dataframe(returns.sort_values(ascending=False).head(10))


# =====================================
# 4️⃣ CORRELATION VIEW
# =====================================

elif view == "Correlation Heatmap":

    st.header("Correlation Heatmap")

    pivot = df.pivot_table(index='date', columns='Ticker', values='close')
    corr = pivot.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.imshow(corr)
    fig.colorbar(cax)

    st.pyplot(fig)


# =====================================
# 5️⃣ RAW DATA VIEW
# =====================================

elif view == "Raw Data":

    st.header("Raw Dataset")

    st.dataframe(df)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="final_data.csv",
        mime="text/csv"
    )
