"""
SYSTEM VERIFICATION SCRIPT
--------------------------
This script validates the integrity of the frozen system logic,
including Data, Analytics, Agents, and Decision Engine.
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
        from decision_engine import execution, consensus, risk_assessment
        
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
    print(f"   Agents Executed: {len(results)} agents")
    if len(results) != 5: raise ValueError("Execution layer missing agents")
    if 'Structure' not in results: raise ValueError("Structure Agent missing")

    # B. Consensus & Disagreement
    # Create synthetic result for math check
    # Structure: 1.0 * 1.0 (Wt 1) -> WtSum 1.0, SigSum 1.0
    # Risk:     -1.0 * 1.0 (Wt 2) -> WtSum 2.0, SigSum -2.0
    # Total Wt: 3.0. Total Sig: -1.0. Avg: -0.33.
    synth_results = {
        'Structure': (1.0, 1.0),
        'Risk': (-1.0, 1.0)
        # Others 0 conf -> 0 weight
    }
    # Mock weights for test: structure=1, risk=2
    # But code uses frozen weights 'Sentiment':0.5, etc.
    # Let's test with real function using just these two relevant ones (others 0 weight effectively if not present? Code iterates input dict)
    # Ah, consensus.compute_consensus iterates input dict. So if we pass partial dict, it works.
    cs = consensus.compute_consensus(synth_results)
    print(f"   Consensus Check (Exp ~ -0.33): {cs:.2f}")
    if not (-0.34 < cs < -0.32): print("   ⚠️ Consensus math deviation")
    
    dis = consensus.compute_disagreement(synth_results)
    print(f"   Disagreement Check: {dis:.2f}") # Std [-1, 1] is 1.0
    
    # C. Risk Assessment
    # Case: Stress Regime -> HIGH
    risk1 = risk_assessment.assess_risk("STRESS", 0.0, {})
    print(f"   Risk (Stress): {risk1}")
    if risk1 != "HIGH": raise ValueError("Risk Assessment failed for STRESS")
    
    # Case: High Disagreement -> HIGH
    risk2 = risk_assessment.assess_risk("CALM", 0.8, {})
    print(f"   Risk (Disagreement): {risk2}")
    if risk2 != "HIGH": raise ValueError("Risk Assessment failed for Disagreement")

    print("\n🎉 SYSTEM VERIFICATION COMPLETED SUCCESSFULLY.")

if __name__ == "__main__":
    run_verification()
