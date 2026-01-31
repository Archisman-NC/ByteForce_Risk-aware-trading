"""
SKEPTIC AGENT
-------------
Actively challenges bullish interpretations.
Biased toward negative signals.
"""

from agent_interface import BaseAgent
from config import settings

class SkepticAgent(BaseAgent):
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates skepticism.
        
        Logic:
        1. Volatility:
           - High Volatility -> Strong Negative Signal.
        2. Trend:
           - Weak Trend (near 0) -> Negative bias (uncertainty).
        
        Constraints:
        - Max Signal <= 0.2 (Never strong positive).
        """
        volatility = feature_row.get('Volatility_20D', 0.0)
        trend = feature_row.get('Trend_Strength_50D', 0.0)
        
        signal = 0.0
        confidence = 0.5 # Base
        
        # 1. Volatility Penalty
        if volatility > settings.VOLATILITY_THRESHOLD_LOW:
            # Scaled negative signal
            # e.g., if vol=2%, low=1%. Ratio=2. Signal -> -1.0 check
            ratio = volatility / settings.VOLATILITY_THRESHOLD_HIGH
            signal -= (ratio * 1.0)
            
        # 2. Trend Skepticism
        # If trend is strong positive, Skeptic remains doubtful (neutral/mild negative)
        # If trend is negative, Skeptic agrees (negative)
        if trend > 0.05:
            # Contrarian fade? Or just restricted?
            # "Biased toward reducing autonomy" -> Dampen positive
            signal -= 0.1
        elif trend < -0.05:
            # Agree with downtrend
            signal -= 0.5
            confidence += 0.2
            
        # Constraints
        signal = max(-1.0, min(0.2, signal))
        confidence = max(0.0, min(1.0, confidence))
        
        return signal, confidence
