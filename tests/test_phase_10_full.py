import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService
import json

def test_phase_10_comprehensive():
    print("🚀 TESTING PHASE 10: COMPREHENSIVE VALIDATION (Persistence + LTM + Journal)")
    print("=" * 50)
    
    service = PersonaService()
    
    # 1. Test Journaling & Optimized Reading
    print("\n[Step 1] Verifying Reflection Journal (Optimized Reading)...")
    service.get_llm_payload("Tell me a story about a lonely robot.")
    service.get_llm_payload("Another message to populate the log.")
    
    insights = service.journal.get_recent_insights(limit=1)
    if insights and "Another message" in insights[0]['context_shorthand']:
        print(f"✅ PASSED: Logic confirmed with optimized tail-read.")
    else:
        print("❌ FAILED: Journal retrieval failed.")

    # 2. Test Memory Filters (Affective Salience)
    print("\n[Step 2] Verifying Memory Salience Bridge...")
    service.fsm.affect.update(delta_p=-1.5, delta_a=-0.2)
    filters = service.get_memory_filters()
    if filters['mood_bias'] == 'melancholic':
        print("✅ PASSED: Mood bias correctly mapped.")
    else:
        print(f"❌ FAILED: Mood bias: {filters['mood_bias']}")

    # 3. Test Persistence with Fragile Labels (The Underscore Test)
    print("\n[Step 3] Verifying Snapshot Persistence (Fragile Labels)...")
    service.fsm.interaction_count = 99
    service.fsm.intimacy_level = 0.88
    
    # Generate a label with multiple underscores to test the new regex/rpartition logic
    complex_label = "stress_test_v10_final_draft"
    snapshot_path = service.save_state(label=complex_label)
    print(f"Saved snapshot with complex label: {complex_label}")
    
    # Create fresh instance and load
    new_service = PersonaService()
    success = new_service.load_state(snapshot_path)
    
    status_post = new_service.fsm.get_status()
    if success and status_post['interaction_count'] == 99 and status_post['intimacy_level'] == 0.88:
        print("✅ PASSED: State restored correctly even with complex labels.")
    else:
        print(f"❌ FAILED: State restoration mismatch: {status_post}")

    # 4. Test Auto-Loading (Latest Snapshot)
    print("\n[Step 4] Verifying Auto-load (Latest)...")
    # Wait a second to ensure a new timestamp if needed (though we'll just check if it picks the complex one we just made)
    auto_success = new_service.load_state() 
    if auto_success and new_service.fsm.interaction_count == 99:
        print("✅ PASSED: Auto-loading correctly identified the latest snapshot.")
    else:
        print("❌ FAILED: Auto-loading failed.")

if __name__ == "__main__":
    test_phase_10_comprehensive()
