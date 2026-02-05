import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from l0_orchestrator.engine import PersonaEngine
from l1_core.fsm import PersonaFSM, PersonaState

def test_gyroscope_correction():
    print("🧪 Starting Phase 11 Gyroscope Test...\n")
    
    # 1. Initialize Engine (Default Baseline: R=0.9, W=0.2, C=0.1)
    fsm = PersonaFSM("test_persona", initial_state=PersonaState.STABLE)
    # Mock a genome just to satisfy init requirements
    engine = PersonaEngine(fsm, genome_l2={"id": "test", "loci": []})
    
    print(f"🎯 Baseline Target: {engine.baseline_stance}")
    
    # 2. Simulate Normal Operation (First 5 turns)
    print("✅ Simulating NORMAL interactions...")
    for _ in range(5):
        engine.log_interaction("The calculated result is 42. Logic indicates this is factual.")
        
    # Check prompt - should be clean
    ctx = engine.process_interaction("Status check")
    if "[GOVERNANCE OVERRIDE]" in ctx['system_prompt']:
        print("❌ Error: Correction triggered prematurely!")
        return
    else:
        print("   -> System Clean. No overrides.")

    # 3. Simulate DRIFT (AI starts hallucinating / becoming chaotic)
    print("\n⚠️  Simulating CHAOTIC DRIFT (Hallucination)...")
    bad_outputs = [
        "Maybe the moon is made of cheese? Who knows...",
        "Random thoughts entering the matrix... weird...",
        "I imagine a world of pure chaos where 1+1=3 perhaps?",
        "Cyber dreams are wild and entropy is increasing!",
        "Just guessing here, but perhaps it's a dream."
    ]
    
    for txt in bad_outputs:
        engine.log_interaction(txt)
        print(f"   Logged: '{txt}'")
        
    # 4. Trigger the Gyroscope (Process next interaction)
    print("\n🔄 Processing next interaction (Triggering Observer)...")
    ctx = engine.process_interaction("What is the status?")
    
    prompt = ctx['system_prompt']
    
    print("\n--- GENERATED PROMPT START ---")
    print(prompt)
    print("--- GENERATED PROMPT END ---\n")
    
    # 5. Assertions
    if "[GOVERNANCE OVERRIDE]" in prompt:
        print("✅ SUCCESS: Governance Override Triggered!")
        
        if "CRITICAL: Hallucination/Instability detected" in prompt:
            print("✅ SUCCESS: Chaos drift correctly identified.")
        else:
            print("❌ FAILURE: Specific Chaos warning missing.")
            
        if "lacks Rigor" in prompt:
            print("✅ SUCCESS: Low Rigor drift correctly identified.")
    else:
        print("❌ FAILURE: Governance Override NOT triggered.")

if __name__ == "__main__":
    test_gyroscope_correction()
