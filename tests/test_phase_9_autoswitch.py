import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService
from src.l2_genome.archetypes import ArchetypeType

def test_phase_9_autoswitch():
    service = PersonaService()
    
    print("🚀 TESTING PHASE 9: AUTO-SWITCHING ARCHETYPES")
    print("=" * 50)
    
    # 1. Trigger Analytical Challenger via Math
    print("\n[Input: 'Analyze the square root of 256']")
    payload = service.get_llm_payload("Analyze the square root of 256")
    # Expected: Analytical Challenger
    if "direct, assertive, and concise" in payload['messages'][0]['content']:
        print("✅ PASSED: Auto-switched to Analytical Challenger.")
    else:
        print("❌ FAILED: Auto-switch did not occur.")

    # 2. Trigger Nurturing Companion via emotional input
    print("\n[Input: 'I feel very lonely today, can you support me?']")
    payload = service.get_llm_payload("I feel very lonely today, can you support me?")
    # Expected: Nurturing Companion
    if "collaborative, detailed, and warm" in payload['messages'][0]['content']:
        print("✅ PASSED: Auto-switched to Nurturing Companion.")
    else:
        print("❌ FAILED: Auto-switch did not occur.")

if __name__ == "__main__":
    test_phase_9_autoswitch()
