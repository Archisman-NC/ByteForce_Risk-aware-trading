"""
DATA PERSISTENCE LAYER
----------------------
This module implements the deterministic local caching of historical data.
It serves as the single source of truth for runtime execution.
"""

import os
import pandas as pd

CACHE_DIR = "data/cache"

def save_to_cache(ticker, df):
    """
    Saves raw OHLCV data to a fixed local CSV file.
    
    Args:
        ticker (str): The stock ticker (e.g., RELIANCE.NS).
        df (pd.DataFrame): The raw data to persist.
    """
    # Ensure cache directory exists
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Fixed file path: data/cache/<ticker>.csv
    file_path = os.path.join(CACHE_DIR, f"{ticker}.csv")
    
    # Flatten MultiIndex columns if present (common with yfinance)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Save as human-readable CSV, no compression
    df.to_csv(file_path)

def load_from_cache(ticker):
    """
    Loads raw OHLCV data from the fixed local cache.
    
    Args:
        ticker (str): The stock ticker to load.
        
    Returns:
        pd.DataFrame: The loaded raw data.
    """
    file_path = os.path.join(CACHE_DIR, f"{ticker}.csv")
    
    # Load with date parsing for index
    # Assumes standard yfinance CSV format where Date is the index/first column
    return pd.read_csv(file_path, index_col=0, parse_dates=True)
