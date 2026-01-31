"""
RISK ASSESSMENT LAYER
---------------------
Determines overall system risk level (LOW, MEDIUM, HIGH).
Conservative override logic.
"""

from config import settings
import regime_detection

RISK_HIGH = "HIGH"
RISK_MEDIUM = "MEDIUM"
RISK_LOW = "LOW"

def assess_risk(regime: str, disagreement: float, feature_row: dict) -> str:
    """
    Assesses overall risk level.
    
    Logic:
    1. HIGH:
       - Regime is STRESS.
       - Disagreement > Threshold (0.40).
       - Drawdown < Max Limit (redundant with Regime=STRESS, but safe).
       
    2. MEDIUM:
       - Regime is VOLATILE.
       - Disagreement > 0.20 (Half Threshold).
       
    3. LOW:
       - Otherwise.
       
    Args:
        regime (str): Detected market regime.
        disagreement (float): Calculated disagreement index.
        feature_row (dict): Raw features (for Drawdown check).
        
    Returns:
        str: LOW, MEDIUM, or HIGH.
    """
    # 1. HIGH RISK CHECKS
    if regime == regime_detection.REGIME_STRESS:
        return RISK_HIGH
        
    if disagreement > settings.DISAGREEMENT_THRESHOLD:
        return RISK_HIGH
        
    drawdown = feature_row.get('Drawdown_20D', 0.0)
    if drawdown < settings.MAX_DRAWDOWN_LIMIT:
        return RISK_HIGH
        
    # 2. MEDIUM RISK CHECKS
    if regime == regime_detection.REGIME_VOLATILE:
        return RISK_MEDIUM
        
    # Medium disagreement (Half of high threshold)
    if disagreement > (settings.DISAGREEMENT_THRESHOLD * 0.5):
        return RISK_MEDIUM
        
    # 3. LOW RISK
    return RISK_LOW
