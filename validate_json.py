"""
JSON VALIDATION SCRIPT
----------------------
Ensures main_simulation output matches schema.
"""

import json
import jsonschema
from main_simulation import run_simulation

def validate():
    print("🔬 VALIDATING JSON OUTPUT...")
    
    # 1. Start Sim and Capture Output
    results = run_simulation()
    
    # 2. Load Schema
    with open('output_schema.json', 'r') as f:
        schema = json.load(f)
        
    # 3. Validate
    try:
        if not isinstance(results, list):
            raise ValueError("Output must be a list of verdicts")
            
        for verdict in results:
            jsonschema.validate(instance=verdict, schema=schema)
            
        print("✅ JSON Schema Validation Passed.")
        
    except jsonschema.ValidationError as e:
        print(f"❌ Schema Validation Failed: {e.message}")
        print(f"   Instance: {e.instance}")
        import sys
        sys.exit(1)
        
if __name__ == "__main__":
    validate()
