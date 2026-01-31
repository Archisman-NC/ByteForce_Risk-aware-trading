"""
HISTORICAL DATA DATA FETCH
--------------------------
This module implements a one-time historical market data acquisition step.
It fetches daily candles for the fixed market universe over a fixed window.
"""

import yfinance as yf
from system_constraints import MARKET_UNIVERSE, TIMEFRAME

def fetch_historical_data():
    """
    Fetches historical OHLCV data for the defined market universe.
    
    Constraints:
    - Fixed Start Date: 2020-01-01
    - Fixed End Date: 2024-01-01
    - Fixed Interval: Daily (1D)
    - No caching or runtime updates.
    
    Returns:
        dict: A dictionary where keys are tickers and values are pandas DataFrames.
    """
    START_DATE = "2020-01-01"
    END_DATE = "2024-01-01"
    
    data_map = {}
    
    # Explicit loop to ensure one fetch per stock
    for ticker in MARKET_UNIVERSE:
        # Reproducible API call with explicit parameters
        df = yf.download(
            tickers=ticker,
            start=START_DATE,
            end=END_DATE,
            interval=TIMEFRAME,
            progress=False,
            auto_adjust=True
        )
        
        # Ensure we have data
        if not df.empty:
            data_map[ticker] = df
            
    return data_map

if __name__ == "__main__":
    # verification execution
    data = fetch_historical_data()
    print(f"Fetched data for: {list(data.keys())}")
    for ticker, df in data.items():
        print(f"{ticker}: {len(df)} rows")
