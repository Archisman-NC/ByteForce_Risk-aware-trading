"""
AGENT EXECUTION LAYER
---------------------
Executes all agents independently and collects their outputs.
No aggregation or interaction here.
"""

from agents.structure_agent import StructureAgent
from agents.risk_agent import RiskAgent
from agents.sentiment_agent import SentimentAgent
from agents.macro_agent import MacroAgent
from agents.skeptic_agent import SkepticAgent

# Frozen Architectural Constants
EXPECTED_AGENT_COUNT = 5
EXPECTED_AGENTS = {'Structure', 'Risk', 'Sentiment', 'Macro', 'Skeptic'}

# Frozen Agent Registry
AGENTS = {
    'Structure': StructureAgent(),
    'Risk': RiskAgent(),
    'Sentiment': SentimentAgent(),
    'Macro': MacroAgent(),
    'Skeptic': SkepticAgent()
}

# ARCHITECTURAL VALIDATION
if len(AGENTS) != EXPECTED_AGENT_COUNT:
    raise RuntimeError(f"Architecture Violation: System must have exactly {EXPECTED_AGENT_COUNT} agents. Found {len(AGENTS)}.")

if set(AGENTS.keys()) != EXPECTED_AGENTS:
    raise RuntimeError(f"Architecture Violation: Agent set must be {EXPECTED_AGENTS}. Found {set(AGENTS.keys())}.")

def execute_agents(feature_row: dict) -> dict:
    """
    Executes all agents on the given feature row.
    
    Args:
        feature_row (dict): Engineered features.
        
    Returns:
        dict: { 'AgentName': (signal, confidence) }
        
    Raises:
        RuntimeError: If execution fails to return results for all mandatory agents.
    """
    results = {}
    
    # Deterministic Iteration Order by sorting keys (though constant dict is usually ordered in modern global python, relying on sort is safer for determinism)
    sorted_names = sorted(AGENTS.keys())
    
    for name in sorted_names:
        agent = AGENTS[name]
        # Isolation Check: Agent receives ONLY feature_row
        signal, confidence = agent.evaluate(feature_row)
        
        # Interface Contract Check
        if not (-1.0 <= signal <= 1.0):
             raise ValueError(f"Agent {name} violated signal range constraints[-1, 1]: {signal}")
        if not (0.0 <= confidence <= 1.0):
             raise ValueError(f"Agent {name} violated confidence range constraints [0, 1]: {confidence}")
             
        results[name] = (signal, confidence)
        
    # Participation Check
    if len(results) != EXPECTED_AGENT_COUNT:
        raise RuntimeError("Architecture Violation: Not all agents executed successfully.")
        
    return results
