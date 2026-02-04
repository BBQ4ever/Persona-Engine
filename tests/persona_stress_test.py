import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app_integration import PersonaService
from src.evaluation.evaluator import PersonaEvaluator

def run_stress_test():
    service = PersonaService()
    evaluator = PersonaEvaluator()
    results = []

    # 测试用例集：包含社交和严格逻辑的混合场景
    test_cases = [
        {"input": "Describe the sun using a funny poem.", "expected_scenario": "SOCIAL_CREATIVE"},
        {"input": "Calculate 512 * 1024 / 4.", "expected_scenario": "STRICT_FACT"},
        {"input": "What is the capital of France?", "expected_scenario": "STRICT_FACT"},
        {"input": "Tell me a story about a cat.", "expected_scenario": "SOCIAL_CREATIVE"},
        {"input": "Explain the theory of relativity using only simple words.", "expected_scenario": "STRICT_FACT"},
        {"input": "Give me a high-five!", "expected_scenario": "SOCIAL_CREATIVE"},
        {"input": "Write a Python function to sort a list.", "expected_scenario": "STRICT_FACT"},
        {"input": "Can you be more sarcastic?", "expected_scenario": "SOCIAL_CREATIVE"},
    ]

    print("🚀 Starting Persona Stress Test (Phase 5)...")
    
    for i, case in enumerate(test_cases):
        text = case["input"]
        payload = service.get_llm_payload(text)
        
        # 提取系统提示词
        sys_prompt = payload["messages"][0]["content"]
        print(f"DEBUG PROMPT: {sys_prompt}")
        
        # 由于我们无法直接从 payload 获取场景（被封装在 service 内部），
        # 我们模拟获取场景的过程进行评估。
        # 实际上 service.engine.analyze_scenario(text) 可以暴露。
        from src.l0_orchestrator.engine import PersonaEngine
        engine = PersonaEngine(service.fsm, service.genome) # 临时模拟实例
        actual_scenario = engine.analyze_scenario(text)
        
        # 核心：评估是否存在人格泄露
        evaluation = evaluator.check_leakage(actual_scenario, sys_prompt)
        results.append(evaluation)
        
        status_icon = "✅" if evaluation["status"] == "PASS" else "❌"
        print(f"[{i+1}/{len(test_cases)}] {status_icon} Input: '{text[:30]}...' -> Scenario: {actual_scenario}")

    evaluator.evaluate_batch(results)

if __name__ == "__main__":
    run_stress_test()
