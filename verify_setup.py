"""
SYSTEM VERIFICATION SCRIPT
--------------------------
This script validates the integrity of the frozen system logic,
including Data, Analytics, Agents, Decision Engine, and Final Output.
"""

import json
import os
import sys

def run_verification():
    print("🔬 STARTING SYSTEM VERIFICATION...\n")
    
    # 1. Imports
    try:
        import system_constraints
        from config import settings
        import data_fetcher
        import data_persistence
        import data_processor
        import feature_engineering
        import regime_detection
        
        # Decision Engine
        from decision_engine import execution, consensus, risk_assessment, final_verdict
        
        print("✅ Core modules loaded successfully.")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)

    # 2. Pipeline Check (Fast)
    print("\n⏳ Testing Data & Analytics...")
    try:
        if not os.path.exists(data_persistence.CACHE_DIR) or len(os.listdir(data_persistence.CACHE_DIR)) < 3:
            data = data_fetcher.fetch_historical_data()
            for t, d in data.items(): data_persistence.save_to_cache(t, d)
        
        ticker = system_constraints.MARKET_UNIVERSE[0]
        df = data_persistence.load_from_cache(ticker)
        df = data_processor.clean_data(df)
        df = feature_engineering.compute_features(df)
        last_row = df.iloc[-1]
        print(f"   ✅ Data Pipeline verified ({len(df)} rows)")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        sys.exit(1)

    # 3. Decision Engine Verification
    print("\n🧠 Testing Decision Engine...")
    
    # A. Execution
    results = execution.execute_agents(last_row)
    if len(results) != 5: raise ValueError("Execution layer missing agents")

    # B. Consensus
    # Real data consensus
    cs = consensus.compute_consensus(results)
    print(f"   Real Data Consensus: {cs:.2f}")
    
    # C. Risk
    # Real data risk
    reg, _ = regime_detection.detect_regime(last_row)
    dis = consensus.compute_disagreement(results)
    risk = risk_assessment.assess_risk(reg, dis, last_row)
    print(f"   Real Data Risk: {risk} (Regime={reg})")
    
    # D. Final Verdict Logic Check
    # Case: Safety Override (High Risk -> HOLD)
    v1, e1, r1 = final_verdict.decide_verdict(0.9, "HIGH")
    if v1 != "HOLD" or e1: raise ValueError("Safety Override failed")
    print("   ✅ Safety Override verified.")
    
    # Case: Buy Signal (Low Risk, High Consensus)
    v2, e2, r2 = final_verdict.decide_verdict(0.8, "LOW")
    if v2 != "BUY" or not e2: raise ValueError("Buy logic failed")
    print("   ✅ Buy Logic verified.")

    print("\n🎉 SYSTEM VERIFICATION COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    run_verification()
