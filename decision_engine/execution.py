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

# Frozen Agent Registry
AGENTS = {
    'Structure': StructureAgent(),
    'Risk': RiskAgent(),
    'Sentiment': SentimentAgent(),
    'Macro': MacroAgent(),
    'Skeptic': SkepticAgent()
}

def execute_agents(feature_row: dict) -> dict:
    """
    Executes all agents on the given feature row.
    
    Args:
        feature_row (dict): Engineered features.
        
    Returns:
        dict: { 'AgentName': (signal, confidence) }
    """
    results = {}
    
    # Deterministic Iteration Order
    for name, agent in AGENTS.items():
        results[name] = agent.evaluate(feature_row)
        
    return results
