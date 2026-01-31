"""
MAIN SIMULATION RUNNER
----------------------
Runs the full intelligence pipeline for the market universe.
Generates final JSON verdicts.
"""

import json
import datetime
import system_constraints
from config import settings
import data_fetcher
import data_persistence
import data_processor
import feature_engineering
import regime_detection
from decision_engine import execution, consensus, risk_assessment, final_verdict

def run_simulation():
    # 1. Ensure Data
    # In a real sim, we might fetch fresh. Here we rely on cache/fetch logic.
    print("--- 🚀 STARTING SIMULATION ---")
    data_map = data_fetcher.fetch_historical_data()
    for t, d in data_map.items():
        data_persistence.save_to_cache(t, d)
        
    results = []
    
    for ticker in system_constraints.MARKET_UNIVERSE:
        # Pipeline
        df = data_persistence.load_from_cache(ticker)
        df_clean = data_processor.clean_data(df)
        df_feat = feature_engineering.compute_features(df_clean)
        
        # Get latest state
        latest_row = df_feat.iloc[-1]
        timestamp = latest_row.name.isoformat()
        
        # 1. Regime
        regime, regime_conf = regime_detection.detect_regime(latest_row)
        
        # 2. Agents
        agent_outputs = execution.execute_agents(latest_row)
        
        # 3. Consensus & Logic
        cons_score = consensus.compute_consensus(agent_outputs)
        disagreement = consensus.compute_disagreement(agent_outputs)
        risk = risk_assessment.assess_risk(regime, disagreement, latest_row)
        
        # 4. Verdict
        action, exec_allowed, reason = final_verdict.decide_verdict(cons_score, risk)
        
        # 5. Assemble JSON
        verdict = {
            "ticker": ticker,
            "timestamp": timestamp,
            "action": action,
            "confidence": regime_conf,
            "is_simulation": True,
            "execution_allowed": exec_allowed,
            "consensus_score": round(cons_score, 4),
            "disagreement_index": round(disagreement, 4),
            "risk_level": risk,
            "regime": regime,
            "regime_confidence": regime_conf,
            "reason": reason
        }
        
        results.append(verdict)
        
    # Output
    output_path = "server/data.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(json.dumps(results, indent=2))
    print(f"\\n✅ Simulation data saved to {output_path}")
    return results

if __name__ == "__main__":
    run_simulation()
