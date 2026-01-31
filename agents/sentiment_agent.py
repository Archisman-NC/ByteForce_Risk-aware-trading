"""
SENTIMENT AGENT
---------------
Simulates sentiment using Volume and Trend proxies.
Bounded by stress constraints.
"""

from agent_interface import BaseAgent
from config import settings
import regime_detection

class SentimentAgent(BaseAgent):
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates sentiment using proxies (Volume Anomaly + Trend).
        
        Logic:
        1. Signal:
           - Positive Anomaly + Positive Trend -> Bullish (+1)
           - Positive Anomaly + Negative Trend -> Bearish (-1)
           - No Anomaly -> Neutral (0)
           
        2. Constraints:
           - If Regime == STRESS: Signal <= 0, Confidence capped at 0.5.
        """
        vol_anomaly = feature_row.get('Volume_Anomaly_20D', 0.0)
        trend = feature_row.get('Trend_Strength_50D', 0.0)
        
        # --- Signal Calculation ---
        # Basic proxy: Volume confirms trend direction
        if abs(vol_anomaly) > 1.0: # Significant volume
            if trend > 0:
                signal = 0.8
            else:
                signal = -0.8
        else:
            signal = 0.0
            
        # Modulation by trend magnitude
        signal += (trend * 5.0) # Add trend bias
        signal = max(-1.0, min(1.0, signal))
        
        # --- Confidence Calculation ---
        # Base confidence on anomaly strength
        confidence = min(1.0, abs(vol_anomaly) / 3.0) # Z=3 is high confidence
        
        # --- Constraints ---
        # Detect regime for constraint checking
        regime, _ = regime_detection.detect_regime(feature_row)
        
        if regime == regime_detection.REGIME_STRESS:
            # Force neutral/negative
            signal = min(0.0, signal)
            # Cap confidence
            confidence = min(0.5, confidence)
            
        return signal, confidence
