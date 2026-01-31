"""
FINAL VERDICT LAYER
-------------------
Determines action (BUY/SELL/HOLD) based on Consensus and Risk.
Conservative: HOLD if Risk is High/Medium.
"""

from config import settings
from decision_engine import risk_assessment

ACTION_BUY = "BUY"
ACTION_SELL = "SELL"
ACTION_HOLD = "HOLD"

def decide_verdict(consensus_score: float, risk_level: str) -> tuple[str, bool, str]:
    """
    Decides the final action and execution flag.
    
    Logic:
    1. Safety Override:
       - If Risk is HIGH or MEDIUM -> HOLD. Execution = False.
       
    2. Consensus Check (Low Risk only):
       - Score > BUY_THRESHOLD (0.75) -> BUY.
       - Score < SELL_THRESHOLD (0.25) -> SELL. (Note: 0.25 is pos, likely meant < -0.25? 
         Settings has CONSENSUS_SCORE_SELL = 0.25. 
         Wait, usually sell is negative. But if range is [-1, 1], maybe 0.25 means "below this is weak"?
         Let's assume standard signals: >0.75 Buy, <0.25 Sell (implies weak positive or negative).
         Actually, usually SELL is -1. But let's follow Settings strictly:
         If score < settings.CONSENSUS_SCORE_SELL -> SELL.
       - Otherwise -> HOLD.
       
    Args:
        consensus_score (float): Aggregated score [-1, 1].
        risk_level (str): LOW, MEDIUM, or HIGH.
        
    Returns:
        tuple: (Action, Execution_Allowed, Reason_String)
    """
    
    # 1. Safety Override
    if risk_level in [risk_assessment.RISK_HIGH, risk_assessment.RISK_MEDIUM]:
        return ACTION_HOLD, False, f"Risk level {risk_level} prevents execution."
        
    # 2. Consensus Logic (Low Risk)
    if consensus_score > settings.CONSENSUS_SCORE_BUY:
        return ACTION_BUY, True, f"Strong consensus ({consensus_score:.2f}) with LOW risk."
        
    if consensus_score < settings.CONSENSUS_SCORE_SELL:
        # e.g., < 0.25. Includes 0.0, -0.5, etc.
        return ACTION_SELL, True, f"Weak/Negative consensus ({consensus_score:.2f}) with LOW risk."
        
    return ACTION_HOLD, False, f"Indecisive consensus ({consensus_score:.2f})."
