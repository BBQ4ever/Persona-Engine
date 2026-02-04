import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService

def test_phase_7_identity():
    service = PersonaService()
    
    print("🚀 TESTING PHASE 7: IDENTITY SUBSTRATE")
    print("=" * 50)
    
    # Test case 1: Masculine bias
    print("\n[TEST: MASCULINE BIAS (0.1)]")
    # Setting identity_signature default to 0.1 manually for testing
    for locus in service.genome['loci']:
        if locus['id'] == 'identity_signature':
            locus['distribution']['values']['default'] = 0.1
            
    payload = service.get_llm_payload("Hello", override_influence=0.0)
    prompt = payload['messages'][0]['content']
    print(f"Prompt output: ...{prompt[-150:]}")
    if "direct, assertive, and concise" in prompt:
        print("✅ PASSED: Masculine bias detected.")
    else:
        print("❌ FAILED: Masculine bias not found.")

    # Test case 2: Feminine bias
    print("\n[TEST: FEMININE BIAS (0.9)]")
    for locus in service.genome['loci']:
        if locus['id'] == 'identity_signature':
            locus['distribution']['values']['default'] = 0.9
            
    payload = service.get_llm_payload("Hello", override_influence=0.0)
    prompt = payload['messages'][0]['content']
    print(f"Prompt output: ...{prompt[-150:]}")
    if "collaborative, detailed, and warm" in prompt:
        print("✅ PASSED: Feminine bias detected.")
    else:
        print("❌ FAILED: Feminine bias not found.")

if __name__ == "__main__":
    test_phase_7_identity()
