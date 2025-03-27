import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Alpha Vantage API Key (Replace with your valid API key)
API_KEY = "R9A0KWPR91D28XCB"

# Predefined list of popular NSE/BSE stocks
stock_options = {
    "Reliance Industries (BSE)": "RELIANCE.BSE",
    "Tata Consultancy Services (BSE)": "TCS.BSE",
    "Infosys (BSE)": "INFY.BSE",
    "HDFC Bank (BSE)": "HDFCBANK.BSE",
    "ICICI Bank (BSE)": "ICICIBANK.BSE",
    "Bharti Airtel (BSE)": "BHARTIARTL.BSE",
    "Larsen & Toubro (BSE)": "LT.BSE",
    "State Bank of India (BSE)": "SBIN.BSE"
}

# Function to fetch stock data
def get_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "Time Series (Daily)" in data:
        df = pd.DataFrame(data["Time Series (Daily)"]).T  # Transpose data
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)  # Convert index to datetime
        df = df.astype(float)  # Convert values to float
        return df
    else:
        return None  # Return None if data is missing or incorrect

# Streamlit UI
st.title("📈 Multi-Stock Analysis (NSE/BSE)")

# Dropdown selection for predefined stocks
selected_stock = st.selectbox("Select a Stock:", list(stock_options.keys()))

# Custom stock symbol input
custom_stock = st.text_input("Or Enter Custom Stock Symbol (e.g., HCLTECH.BSE):")

# Determine final stock symbol to use
if custom_stock:
    stock_symbol = custom_stock
else:
    stock_symbol = stock_options[selected_stock]

# Button to fetch data
if st.button("Fetch Data"):
    stock_data = get_stock_data(stock_symbol)
    
    if stock_data is not None:
        st.success(f"✅ Showing data for **{stock_symbol}**")
        st.write(stock_data.head())  # Show first few rows
        
        if "Close" in stock_data.columns:
            # Plot stock closing prices
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(stock_data.index, stock_data["Close"], label="Close Price", color="blue")
            ax.set_title(f"{stock_symbol} Closing Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (INR)")
            ax.legend()
            st.pyplot(fig)
        else:
            st.error("❌ 'Close' column not found in stock data.")
    else:
        st.error("❌ Failed to fetch stock data. Check API key and stock symbol.")
