"""
FROZEN NUMERIC THRESHOLDS
-------------------------
This file defines the immutable numeric constants for the deterministic simulation.
These values are permanently locked and must not be altered.
"""

# Risk & Volatility Thresholds
VOLATILITY_THRESHOLD_HIGH = 0.025  # Daily return std dev > 2.5%
VOLATILITY_THRESHOLD_LOW = 0.010   # Daily return std dev < 1.0%

# Drawdown Limits
MAX_DRAWDOWN_LIMIT = -0.15         # Max allowable drawdown (-15%)

# Consensus Logic Thresholds
CONSENSUS_SCORE_BUY = 0.75         # Minimum score to trigger BUY
CONSENSUS_SCORE_SELL = 0.25        # Maximum score to trigger SELL
DISAGREEMENT_THRESHOLD = 0.40      # Max variance allowed between agents

# Execution Gating
MIN_CONFIDENCE_LEVEL = 0.80        # Minimum confidence required for action
