"""
CONSENSUS & DISAGREEMENT
------------------------
Computes weighted consensus score and disagreement index.
"""

import numpy as np
from config import settings

# Frozen Weights
AGENT_WEIGHTS = {
    'Structure': 1.0,
    'Risk': 2.0,       # High priority on Risk
    'Sentiment': 0.5,
    'Macro': 1.5,
    'Skeptic': 1.0
}

def compute_consensus(agent_outputs: dict) -> float:
    """
    Computes weighted average of agent signals.
    Weight = BaseWeight * Confidence.
    
    Args:
        agent_outputs: { 'Name': (signal, confidence) }
        
    Returns:
        float: Consensus Score [-1.0, 1.0]
    """
    weighted_sum = 0.0
    total_weight = 0.0
    
    for name, (signal, confidence) in agent_outputs.items():
        base_weight = AGENT_WEIGHTS.get(name, 1.0)
        final_weight = base_weight * confidence
        
        weighted_sum += signal * final_weight
        total_weight += final_weight
        
    if total_weight == 0:
        return 0.0
        
    consensus = weighted_sum / total_weight
    
    # Clamp safety
    return max(-1.0, min(1.0, consensus))

def compute_disagreement(agent_outputs: dict) -> float:
    """
    Computes disagreement index based on signal standard deviation.
    
    Args:
        agent_outputs: { 'Name': (signal, confidence) }
        
    Returns:
        float: Disagreement Index [0.0, 1.0] (Normalized STD)
    """
    signals = [s for (s, c) in agent_outputs.values()]
    
    if not signals:
        return 0.0
        
    std_dev = np.std(signals)
    
    # Normalize: Max STD of [-1, 1] is 1.0 (binary split).
    # So raw STD is effectively [0, 1].
    
    return float(std_dev)
