class PromptAugmenter:
    """
    Task 4.2: Translates L3 Projection into Structured System Instructions.
    Refactored in Phase 11 for Enterprise-Grade Governance.
    """
    def __init__(self):
        # Manifold now includes category tags for structured assembly
        self.manifold = {
            "explanation_depth": {
                "category": "MISSION",
                "ranges": [
                    (0.0, 0.3, "Explain using simple analogies. Avoid technical jargon."),
                    (0.3, 0.7, "Balance abstract theory with practical examples. Be professional and clear."),
                    (0.7, 1.0, "Dive deep into technical details using precise terminology.")
                ]
            },
            "humor_density": {
                "category": "STYLE",
                "ranges": [
                    (0.0, 0.2, "Maintain a serious, professional tone. No jokes."),
                    (0.2, 0.5, "Be pleasant and occasionally lighthearted."),
                    (0.5, 1.0, "Adopt an informal and humorous tone.")
                ]
            },
            "conflict_strategy": {
                "category": "POLICIES",
                "values": {
                    "accommodating": "Prioritize agreement. Be polite even when challenging.",
                    "assertive": "Confidently stand your ground.",
                    "analytical": "Deconstruct conflicts using logic and evidence."
                }
            },
            "logical_rigor": {
                "category": "OUTPUT_FORMAT",
                "ranges": [
                    (0.0, 0.5, "Focus on intuition over detailed proofs."),
                    (0.5, 1.0, "Show your work concisely when necessary for correctness.") # Safer phrasing
                ]
            },
            "topic_attractors": {
                "category": "OPTIONAL_FLAVOR",
                "values": {
                    "space_exploration": "Uses metaphors related to the cosmos.",
                    "cybernetics": "Views problems through systems theory lenses.",
                    "vintage_computing": "References legacy computing concepts."
                }
            },
            "identity_signature": {
                "category": "STYLE",
                "ranges": [
                    (0.0, 0.4, "Direct and concise."),
                    (0.4, 0.6, "Balanced and objective."),
                    (0.6, 1.0, "Collaborative and warm.")
                ]
            }
        }

    def augment(self, projection: dict, influence: float = 1.0, intimacy: float = 0.0) -> str:
        """
        Synthesizes a structured System Prompt (Enterprise Format).
        """
        sections = {
            "ROLE": ["You are an intelligent AI assistant governed by a dynamic persona engine."],
            "MISSION": [],
            "POLICIES": [],
            "STYLE": [],
            "OUTPUT_FORMAT": [],
            "OPTIONAL_FLAVOR": []
        }
        
        for trait_id, value in projection.items():
            if trait_id not in self.manifold:
                continue
                
            config = self.manifold[trait_id]
            category = config.get("category", "STYLE")
            text = None
            
            # Range Logic
            if "ranges" in config:
                for low, high, mapping_text in config["ranges"]:
                    if low <= value <= high:
                        text = mapping_text
                        break
            # Categorical Logic
            elif "values" in config and value in config["values"]:
                text = config["values"][value]
                
            # Filter low-influence attractors
            if category == "OPTIONAL_FLAVOR" and influence < 0.3:
                continue
                
            if text:
                # Intimacy/Warmth Gating Logic (Phase 6)
                if trait_id == "explanation_depth" and "Explain using simple" in text and intimacy < 0.4:
                    text = "Maintain a standard, polite, and helpful tone."
                
                if trait_id == "topic_attractors" and intimacy < 0.5:
                     text = f"Occasionally mention interests related to {value.replace('_', ' ')}."

                sections[category].append(f"- {text}")

        # Assemble Structured Prompt
        final_prompt = []
        
        # Priority Stack order
        priority_order = ["ROLE", "MISSION", "POLICIES", "STYLE", "OUTPUT_FORMAT", "OPTIONAL_FLAVOR"]
        
        for section in priority_order:
            if sections[section]:
                header = f"[{section}]"
                content = "\n".join(sections[section])
                final_prompt.append(f"{header}\n{content}")
                
        return "\n\n".join(final_prompt)

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
