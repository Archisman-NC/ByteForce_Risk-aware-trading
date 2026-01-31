"""
MACRO AGENT
-----------
Assesses broad market context via regime detection.
Prevents tunnel vision.
"""

from agent_interface import BaseAgent
import regime_detection

class MacroAgent(BaseAgent):
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates macro context based on Regime.
        
        Logic:
        - STRESS: Signal -1.0, High Confidence.
        - VOLATILE: Signal -0.5, Medium Confidence.
        - CALM: Signal +0.5, High Confidence.
        - TRANSITION: Signal 0.0, Low Confidence.
        """
        regime, _ = regime_detection.detect_regime(feature_row)
        
        if regime == regime_detection.REGIME_STRESS:
            return -1.0, 0.9
        elif regime == regime_detection.REGIME_VOLATILE:
            return -0.5, 0.6
        elif regime == regime_detection.REGIME_CALM:
            return 0.5, 0.8
        else: # TRANSITION
            return 0.0, 0.4
