import os
import sys
import random
from src.app_integration import PersonaService

def run_background_tests():
    service = PersonaService()
    
    test_cases = [
        {
            "desc": "LOW INTIMACY (Stranger) - Bandwidth Gating Check", 
            "influence": 1.0, 
            "intimacy": 0.2, 
            "input": "Explain this complex topic.",
            "check": "Occasionally mention" # For attractors at low intimacy
        },
        {
            "desc": "HIGH INTIMACY (Close) - Full Expression Check", 
            "influence": 1.0, 
            "intimacy": 0.9, 
            "input": "Tell me a joke.",
            "check": "cybernetics and system theory" # Full disclosure for attractors
        },
        {
            "desc": "STRICT SCENARIO (Math) - Influence Gating Check", 
            "influence": None, 
            "intimacy": 1.0, 
            "input": "calculate 2+2",
            "check_not": "interests related to"
        },
        {
            "desc": "CATEGORICAL ATTRACTOR GATING",
            "influence": 1.0,
            "intimacy": 0.2,
            "input": "Social talk",
            "check": "Occasionally mention" # Should be downgraded Disclosure
        }
    ]

    print("🚀 STARTING BACKGROUND VALIDATION SUITE\n" + "="*50)

    for i, case in enumerate(test_cases):
        print(f"\n[TEST #{i+1}] {case['desc']}")
        
        # Setup state
        service.fsm.intimacy_level = case['intimacy']
        
        # Execute
        payload = service.get_llm_payload(case['input'], override_influence=case['influence'])
        system_prompt = payload['messages'][0]['content']
        
        print(f"--- Prompt Output ---")
        print(system_prompt)
        print(f"---------------------")
        
        # Simple assertions
        if "check" in case:
            if case['check'] in system_prompt:
                print(f"✅ PASSED: Found expected text '{case['check']}'")
            else:
                print(f"❌ FAILED: Did not find '{case['check']}'")
        
        if "check_not" in case:
            if case['check_not'] in system_prompt:
                print(f"❌ FAILED: Found restricted text '{case['check_not']}'")
            else:
                print(f"✅ PASSED: Restricted text '{case['check_not']}' correctly excluded.")

    print("\n" + "="*50 + "\n✅ ALL BACKGROUND VALIDATIONS DONE.")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    run_background_tests()
