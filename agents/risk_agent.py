"""
RISK AGENT
----------
Assesses downside risk using drawdown and volatility.
Conservative design: biased toward negative signals.
"""

from agent_interface import BaseAgent
from config import settings

class RiskAgent(BaseAgent):
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates risk.
        
        Logic:
        1. Drawdown:
           - Deeper drawdown (more negative) -> Stronger negative signal.
           - If Drawdown <= MAX_DRAWDOWN_LIMIT (-15%), Signal = -1.0.
           
        2. Volatility:
           - Higher volatility -> Lower confidence.
           - Penalty factor similar to StructureAgent.
        
        Constraint: Never emit positive signal (Range [-1.0, 0.0]).
        """
        drawdown = feature_row.get('Drawdown_20D', 0.0)
        volatility = feature_row.get('Volatility_20D', 0.0)
        
        # --- Signal Calculation ---
        # Drawdown is negative. We want negative signal as it gets deeper.
        # Normalize against limit (e.g., -0.15)
        limit_dd = settings.MAX_DRAWDOWN_LIMIT # e.g. -0.15
        
        if drawdown <= limit_dd:
            signal = -1.0
        elif drawdown >= 0:
            signal = 0.0
        else:
            # Linear mapping: 0 -> 0, Limit -> -1
            signal = -1.0 * (drawdown / limit_dd)
            
        # Clamp to [-1.0, 0.0] ensuring conservative bias
        signal = max(-1.0, min(0.0, signal)) * -1.0 # Wait, logic error in scaling above?
        # Let's re-verify:
        # DD = -0.075 (Half limit). limit = -0.15.
        # Ratio = -0.075 / -0.15 = 0.5.
        # Signal should be -0.5.
        # Code: signal = -1.0 * (0.5) = -0.5. Correct.
        # Wait, if dd = -0.075, signal is -0.5.
        # max(-1.0, min(0.0, -0.5)) -> -0.5. Correct.
        # But wait, did I multiply by -1.0 at end? NO, remove that.
        
        signal = max(-1.0, min(0.0, -1.0 * (drawdown / limit_dd)))
        
        # --- Confidence Calculation ---
        # Penalize for volatility
        limit_vol = settings.VOLATILITY_THRESHOLD_HIGH
        if limit_vol <= 0:
             penalty = 1.0
        else:
             penalty = volatility / limit_vol
             
        confidence = max(0.0, 1.0 - penalty)
        
        return signal, confidence
