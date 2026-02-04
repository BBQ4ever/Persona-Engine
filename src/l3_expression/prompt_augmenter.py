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
            ]
        }

    def augment(self, projection: dict) -> str:
        """
        根据采样结果，合成 System Prompt。
        """
        instructions = []
        
        for trait_id, value in projection.items():
            if trait_id not in self.manifold:
                continue
                
            mapping = self.manifold[trait_id]
            
            if isinstance(mapping, list):
                # 处理范围映射 (Range Loci)
                for low, high, text in mapping:
                    if low <= value <= high:
                        instructions.append(f"- {text}")
                        break
            elif isinstance(mapping, dict):
                # 处理分类映射 (Categorical Loci)
                if value in mapping:
                    instructions.append(f"- {mapping[value]}")
                    
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
