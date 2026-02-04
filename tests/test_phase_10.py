import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService
import time

def test_phase_10_persistence():
    print("🚀 TESTING PHASE 10: MULTI-SESSION COHERENCE (PERSISTENCE)")
    print("=" * 50)
    
    # 1. Initialize and mutate state
    service = PersonaService()
    print("\n[Step 1] Creating initial state...")
    service.fsm.record_interaction()
    service.fsm.record_interaction()
    service.fsm.affect.update(delta_p=0.5, delta_a=-0.2)
    service.fsm.intimacy_level = 0.65
    
    status_pre = service.fsm.get_status()
    print(f"Pre-save status: Interactions={status_pre['interaction_count']}, Affect={status_pre['affect']}, Intimacy={status_pre['intimacy_level']}")

    # 2. Save Snapshot
    print("\n[Step 2] Saving snapshot...")
    snapshot_path = service.save_state(label="test_v10")
    
    # 3. Create fresh service and load
    print("\n[Step 3] Loading into a fresh service instance...")
    new_service = PersonaService()
    new_service.load_state(snapshot_path)
    
    status_post = new_service.fsm.get_status()
    print(f"Post-load status: Interactions={status_post['interaction_count']}, Affect={status_post['affect']}, Intimacy={status_post['intimacy_level']}")

    # 4. Verify
    if status_post['interaction_count'] == 2 and status_post['intimacy_level'] == 0.65:
        print("\n✅ PASSED: FSM state restored correctly.")
    else:
        print("\n❌ FAILED: FSM state mismatch.")
        
    if abs(status_post['affect']['p'] - 0.5) < 0.01:
        print("✅ PASSED: Affective manifold restored correctly.")
    else:
        print("❌ FAILED: Affective state mismatch.")

if __name__ == "__main__":
    test_phase_10_persistence()
