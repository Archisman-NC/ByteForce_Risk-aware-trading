"""
MARKET REGIME DETECTION
-----------------------
This module implements priority-based deterministic market regime detection.
It uses frozen thresholds to classify the market state into 4 regimes.
"""

from config import settings

# Regime Constants
REGIME_STRESS = "STRESS"
REGIME_VOLATILE = "VOLATILE"
REGIME_CALM = "CALM"
REGIME_TRANSITION = "TRANSITION"

def detect_regime(feature_row):
    """
    Detects the market regime for a single timestamp based on features.
    
    Priority Logic:
    1. STRESS: If Drawdown < MAX_DRAWDOWN_LIMIT (e.g., < -15%)
    2. VOLATILE: If Volatility > HIGH_THRESHOLD (e.g., > 2.5%)
    3. CALM: If Volatility < LOW_THRESHOLD (e.g., < 1.0%)
    4. TRANSITION: All other cases.
    
    Args:
        feature_row (pd.Series or dict): Row containing 'Drawdown_20D' and 'Volatility_20D'.
        
    Returns:
        tuple: (Regime Name (str), Confidence (float))
    """
    # Extract required features
    drawdown = feature_row['Drawdown_20D']
    volatility = feature_row['Volatility_20D']
    
    # 1. CHECK STRESS (Highest Priority)
    # MAX_DRAWDOWN_LIMIT is negative (e.g., -0.15)
    # If drawdown is deeper (more negative) than limit, it's STRESS
    if drawdown < settings.MAX_DRAWDOWN_LIMIT:
        return REGIME_STRESS, 1.0
        
    # 2. CHECK VOLATILE
    if volatility > settings.VOLATILITY_THRESHOLD_HIGH:
        return REGIME_VOLATILE, 1.0
        
    # 3. CHECK CALM
    if volatility < settings.VOLATILITY_THRESHOLD_LOW:
        return REGIME_CALM, 1.0
        
    # 4. DEFAULT TO TRANSITION
    return REGIME_TRANSITION, 0.5
