import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService

def test_phase_9_fluid_stance():
    service = PersonaService()
    
    print("🚀 TESTING PHASE 9: FLUID STANCE (R.W.C MODEL)")
    print("=" * 50)
    
    # 1. Test Rigor Mapping
    print("\n[TEST: HIGH RIGOR (0.9, 0.2, 0.1)]")
    service.set_stance(rigor=0.9, warmth=0.2, chaos=0.1)
    payload = service.get_llm_payload("Technical review.", override_influence=1.0)
    prompt = payload['messages'][0]['content']
    print(f"DEBUG PROMPT:\n{prompt}")
    
    # Check if correct descriptions are loaded
    if "Deconstruct conflicts using logic and evidence" in prompt and "direct, assertive, and concise" in prompt:
         print("✅ PASSED: High rigor successfully mapped to analytical DNA.")
    else:
         print("❌ FAILED: Mapping incorrect.")

    # 2. Test Warmth & Affect Integration
    print("\n[TEST: HIGH WARMTH (0.2, 0.9, 0.3)]")
    service.set_stance(rigor=0.2, warmth=0.9, chaos=0.3)
    affect = service.fsm.get_status()['affect']
    print(f"Affect Baseline: {affect}")
    
    if affect['p'] > 0.4: # Warmth 0.9 -> P ~ 0.52
         print("✅ PASSED: High warmth correctly shifted Pleasure baseline.")
    else:
         print("❌ FAILED: Affective baseline not synced.")

    # 3. Test Auto-Switching via Stance
    print("\n[TEST: ENGINE AUTO-STANCE]")
    # Scenario: Social Support -> Should trigger High Warmth stance
    payload = service.get_llm_payload("I need some support and comfort.")
    prompt = payload['messages'][0]['content']
    
    if "collaborative, detailed, and warm" in prompt:
         print("✅ PASSED: Engine correctly projected 'Social Support' to 'Warm Stance'.")
    else:
         print("❌ FAILED: Auto-stance failed.")

if __name__ == "__main__":
    test_phase_9_fluid_stance()
