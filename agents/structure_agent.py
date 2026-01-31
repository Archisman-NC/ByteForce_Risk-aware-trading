"""
STRUCTURE AGENT
---------------
Evaluates price structure using trend and volatility features.
Signal increases with trend strength.
Confidence decreases with volatility.
"""

from agent_interface import BaseAgent
from config import settings

class StructureAgent(BaseAgent):
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates market structure.
        
        Logic:
        1. Signal comes from Trend_Strength_50D.
           - Scaled s.t. 10% deviation (+0.10) => +1.0 signal.
           - Clamped to [-1.0, 1.0].
           
        2. Confidence comes from Volatility_20D.
           - Linear decay based on VOLATILITY_THRESHOLD_HIGH.
           - Volatility >= High Threshold => Confidence 0.0.
           - Volatility near 0 => Confidence 1.0.
        """
        trend = feature_row.get('Trend_Strength_50D', 0.0)
        volatility = feature_row.get('Volatility_20D', 0.0)
        
        # --- Signal Calculation ---
        # Scale: 0.10 trend (10%) = 1.0 signal
        raw_signal = trend * 10.0
        # Clamp to [-1.0, 1.0]
        signal = max(-1.0, min(1.0, raw_signal))
        
        # --- Confidence Calculation ---
        # Volatility penalty
        # If vol >= 2.5%, confidence = 0
        limit = settings.VOLATILITY_THRESHOLD_HIGH
        if limit <= 0:
            # Defensive check, though constant is fixed > 0
            penalty_factor = 1.0 
        else:
            penalty_factor = volatility / limit
            
        confidence = max(0.0, 1.0 - penalty_factor)
        
        return signal, confidence
