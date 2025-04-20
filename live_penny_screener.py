import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# -------------------------
# Helper Functions
# -------------------------
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(page_title="Live Penny Stock Screener", layout="wide")
st.title("Live Penny Stock Screener")

# Manual refresh
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# -------------------------
# User Inputs
# -------------------------
with st.sidebar:
    st.header("Screener Criteria")
    max_price = st.number_input("Max Price ($)", value=5.0, step=0.5)
    min_volume = st.number_input("Min Volume", value=500_000)
    max_rsi = st.slider("Max RSI", 0, 100, 70)
    history_period = st.selectbox("History Period", options=["1y", "6mo", "3mo"], index=0)
    tickers_text = st.text_area(
        "Tickers (comma-separated)",
        value="SNDL, NOK, BBIG, ZOM, TLRY, PLTR, AMC, GME"
    )

tickers = [t.strip().upper() for t in tickers_text.split(",") if t.strip()]

# -------------------------
# Data Fetch & Calculation
# -------------------------
results = []
for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=history_period)
    if hist.empty or len(hist) < 15:
        continue

    latest = hist.iloc[-1]
    price = latest['Close']
    volume = latest['Volume']
    avg_vol = hist['Volume'].tail(20).mean()
    rel_vol = volume / avg_vol if avg_vol > 0 else 0
    change_pct = ((latest['Close'] - latest['Open']) / latest['Open']) * 100
    rsi = calculate_rsi(hist).iloc[-1]

    # Placeholder float (replace with real source)
    sample_float = 50_000_000

    if (
        price <= max_price and
        volume >= min_volume and
        rsi <= max_rsi
    ):
        results.append({
            'Ticker': ticker,
            'Price ($)': round(price, 2),
            'Volume': volume,
            'RelVol': round(rel_vol, 2),
            'Change (%)': round(change_pct, 2),
            'RSI': round(rsi, 2),
            'Float': sample_float
        })

# -------------------------
# Display Results
# -------------------------
if results:
    df = pd.DataFrame(results)
    st.dataframe(df)
else:
    st.info("No stocks met the current criteria.")

st.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
