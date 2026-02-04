from src.app_integration import PersonaService
import time

def test_phase_8_emotions():
    service = PersonaService()
    
    print("🚀 TESTING PHASE 8: EMOTIONAL MANIFOLD (PAD)")
    print("=" * 50)
    
    # Check baseline
    print(f"\n[Baseline] {service.fsm.get_status()['affect']}")
    
    # 场景: 社交互动让 AI 心情变好
    print("\n[Scenario: Positive Social Interactions]")
    for i in range(5):
        service.get_llm_payload("You are doing great!", session_id="test_user")
        affect = service.fsm.get_status()['affect']
        print(f"Interaction {i+1} - Affect: {affect}")
        
    # Check if Pleasure (p) increased
    if service.fsm.affect.p > 0:
        print("✅ PASSED: Pleasure increased via social interaction.")
    else:
        print("❌ FAILED: Pleasure did not increase.")

    # 场景: 模拟外部压力脉冲 (手动注入)
    print("\n[Scenario: External Stress Pulse]")
    service.fsm.affect.update(delta_p=-0.5, delta_a=0.8, delta_d=-0.3)
    affect = service.fsm.get_status()['affect']
    print(f"After Stress: {affect}")
    
    warp = service.fsm.affect.get_warp_factors()
    print(f"Current Warp Factors: {warp}")
    
    if warp['variability_warp'] > 1.2:
         print("✅ PASSED: High arousal increased variability warp.")

    # 场景: 衰减测试
    print("\n[Scenario: Emotional Decay]")
    for i in range(3):
        service.get_llm_payload("Checking decay...", session_id="test_user")
        affect = service.fsm.get_status()['affect']
        print(f"Decay Step {i+1} - Affect: {affect}")

if __name__ == "__main__":
    test_phase_8_emotions()
