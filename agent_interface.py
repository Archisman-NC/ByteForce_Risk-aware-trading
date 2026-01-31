"""
AGENT INTERFACE
---------------
This module defines the mandatory interface for all independent AI agents.
It checks for compliance with input/output constraints.
"""

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for deterministic market agents.
    Constraints:
    - Input: Structured feature dictionary/Series.
    - Output: (signal, confidence).
    - Stateless and side-effect free.
    """
    
    @abstractmethod
    def evaluate(self, feature_row: dict) -> tuple[float, float]:
        """
        Evaluates features to produce a signal and confidence.
        
        Args:
            feature_row (dict): A row of engineered features.
            
        Returns:
            tuple[float, float]:
                - signal: Range [-1.0, 1.0] (Sell < 0 < Buy)
                - confidence: Range [0.0, 1.0] (Low < High)
        """
        pass
