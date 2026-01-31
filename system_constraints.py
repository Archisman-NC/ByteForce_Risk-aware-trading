"""
FROZEN MARKET SCOPE
-------------------
This file defines the hard system constraints for the deterministic financial simulation.
These values are permanently locked and must not be altered by runtime configuration,
environment variables, or user input.
"""

# Market Universe: Fixed list of supported equities
MARKET_UNIVERSE = (
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS"
)

# Exchange: Immutable exchange identifier
EXCHANGE = "NSE"

# Timeframe: Immutable candle timeframe
TIMEFRAME = "1D"

# Execution Mode: Simulation only, no live trading
EXECUTION_MODE = "SIMULATION"
