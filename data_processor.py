"""
DATA CLEANING LOGIC
-------------------
This module implements the deterministic cleaning of cached market data.
It prepares the data for analysis without altering the raw cache.
"""

import pandas as pd

def clean_data(df):
    """
    Cleans the raw OHLCV data for deterministic simulation.
    
    Rules:
    - Sort strictly by date (ascending).
    - Remove rows with missing/invalid values.
    - Compute 'Daily_Return' as % change of Close.
    - No smoothing or imputation.
    
    Args:
        df (pd.DataFrame): The raw dataframe loaded from cache.
        
    Returns:
        pd.DataFrame: The cleaned and prepared dataframe.
    """
    # 1. Sort strictly by date (index)
    df = df.sort_index(ascending=True)
    
    # 2. Remove rows with any original missing values
    df = df.dropna()
    
    # 3. Compute Daily Returns (simple % change of Close)
    # We use 'Close' for return calculation as standard convention
    df['Daily_Return'] = df['Close'].pct_change()
    
    # 4. Remove rows created by return calculation (e.g., first row becomes NaN)
    df = df.dropna()
    
    return df
