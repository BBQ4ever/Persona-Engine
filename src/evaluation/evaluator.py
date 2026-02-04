import re

class PersonaEvaluator:
    """
    Phase 5: 自动化评测模块。
    用于检测“人格泄露”（Persona Leakage）以及人格一致性。
    """
    def __init__(self):
        # 敏感词库：用于识别高强度人格表达的关键词
        self.personality_markers = [
            "joke", "pun", "sarcasm", "wit", "humorous", "metaphor", "playful", "informal"
        ]

    def check_leakage(self, scenario_type: str, system_prompt: str) -> dict:
        """
        检测在严谨模式下是否发生了人格泄露。
        Leakage = (Scenario is STRICT_FACT) AND (Prompt contains personality markers)
        """
        is_leakage = False
        findings = []
        
        if scenario_type == "STRICT_FACT":
            prompt_lower = system_prompt.lower()
            # 改进：仅当关键词出现且不包含 "no" 或 "avoid" 等否定词时才视为泄露
            for marker in self.personality_markers:
                if re.search(rf"\b{marker}\b", prompt_lower):
                    # 改进：更鲁棒的否定词检测
                    # 检查 marker 前面 50 个字符内是否含有否定词
                    marker_idx = prompt_lower.find(marker)
                    context_window = prompt_lower[max(0, marker_idx-50):marker_idx]
                    if re.search(r"(no|avoid|without|serious|not|don't)", context_window):
                        print(f"DEBUG EVAL: Found negation for '{marker}' in context: '...{context_window}'")
                    else:
                        is_leakage = True
                        findings.append(f"Leakage detected: Personality instruction '{marker}' found without negation.")
        
        return {
            "status": "FAIL" if is_leakage else "PASS",
            "scenario": scenario_type,
            "leakage_detected": is_leakage,
            "findings": findings
        }

    def evaluate_batch(self, test_results: list):
        """
        批量评估测试运行结果。
        """
        total = len(test_results)
        passed = sum(1 for r in test_results if r["status"] == "PASS")
        leakage_count = sum(1 for r in test_results if r["leakage_detected"])
        
        print("\n" + "="*40)
        print("📊 PERSONA ENGINE STRESS TEST REPORT")
        print("="*40)
        print(f"Total Test Cases: {total}")
        print(f"Passed:           {passed}")
        print(f"Failed:           {total - passed}")
        print(f"Leakage Incidents: {leakage_count}")
        print(f"Success Rate:     {(passed/total * 100):.2f}%")
        print("="*40)

if __name__ == "__main__":
    # 模拟测试
    evaluator = PersonaEvaluator()
    
    # CASE 1: 成功的隔离
    res1 = evaluator.check_leakage("STRICT_FACT", "Maintain a professional tone.")
    print(f"Test 1: {res1['status']}")
    
    # CASE 2: 发生泄露
    res2 = evaluator.check_leakage("STRICT_FACT", "Use jokes and puns.")
    print(f"Test 2: {res2['status']} - {res2['findings']}")
