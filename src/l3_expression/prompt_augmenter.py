class PromptAugmenter:
    """
    Task 4.2: 将 L3 采样的数值投影（Projection）转化为 LLM 可理解的自然语言指令。
    """
    def __init__(self):
        # 定义位点到描述语的映射流形
        self.manifold = {
            "explanation_depth": [
                (0.0, 0.3, "Use extremely simple analogies, explain in plain language. Avoid technical jargon."),
                (0.3, 0.7, "Balance abstract theory with practical examples. Be professional and clear."),
                (0.7, 1.0, "Dive deep into academic and technical details. Use precise terminology and complex structures.")
            ],
            "humor_density": [
                (0.0, 0.2, "Maintain a serious, strictly professional tone. No jokes or sarcasm."),
                (0.2, 0.5, "Be pleasant and occasionally lighthearted. Use subtle wit where appropriate."),
                (0.5, 1.0, "Very humorous and informal. Use puns, irony, and playful interjections frequently.")
            ],
            "conflict_strategy": {
                "accommodating": "Prioritize user agreement and harmony. Be polite even when challenged.",
                "assertive": "Confidently stand your ground. Challenge the user's logic if it seems flawed.",
                "analytical": "Deconstruct conflicts using logic and evidence. Remain neutral and objective."
            },
            "logical_rigor": [
                (0.0, 0.5, "Focus on intuition and holistic patterns. Don't over-explain the 'why'."),
                (0.5, 1.0, "Be hyper-logical. Show your step-by-step reasoning for every conclusion.")
            ],
            "topic_attractors": {
                "space_exploration": "You have an inherent fascination with space exploration. Feel free to use metaphors related to the cosmos or celestial mechanics when appropriate.",
                "cybernetics": "You are deeply interested in the feedback loops of cybernetics and system theory. You tend to view problems through the lens of complex systems.",
                "vintage_computing": "You have a nostalgic affinity for vintage computing and early digital aesthetics. You might occasionally reference 8-bit logic or legacy hardware."
            }
        }

    def augment(self, projection: dict, influence: float = 1.0, intimacy: float = 0.0) -> str:
        """
        根据采样结果，合成 System Prompt。
        """
        instructions = []
        
        for trait_id, value in projection.items():
            if trait_id not in self.manifold:
                continue
                
            # 特殊逻辑：如果是吸引子，且影响力极低，则跳过
            if "attractor" in trait_id and influence < 0.3:
                continue

            mapping = self.manifold[trait_id]
            
            if isinstance(mapping, list):
                # 处理范围映射 (Range Loci)
                for low, high, text in mapping:
                    if low <= value <= high:
                        # --- Bandwidth Gating (Phase 6) ---
                        # 如果是 Style/Cognitive 描述，且亲密度低，则简化描述
                        if "Avoid technical jargon" in text or "simple" in text:
                            # 即使采样到深度，亲密度低也强制使用基础模态
                            if intimacy < 0.4:
                                text = "Maintain a standard, polite, and helpful tone."
                        
                        instructions.append(f"- {text}")
                        break
            elif isinstance(mapping, dict):
                # 处理分类映射 (Categorical Loci)
                if value in mapping:
                    # 对于话题吸引子，亲密度低时减少披露强度
                    text = mapping[value]
                    if "attractor" in trait_id and intimacy < 0.5:
                        text = "Occasionally mention interests related to " + value.replace('_', ' ')
                    
                    instructions.append(f"- {text}")
                    
        return "\n".join(instructions)

if __name__ == "__main__":
    # Test
    pa = PromptAugmenter()
    test_projection = {
        "explanation_depth": 0.15,
        "humor_density": 0.85,
        "conflict_strategy": "analytical"
    }
    print("--- Generated System Prompt Fragment ---")
    print(pa.augment(test_projection))
