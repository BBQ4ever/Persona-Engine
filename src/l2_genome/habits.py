import random
from typing import List, Dict

class HabitGenerator:
    """
    Generates 'Synthetic' habits and quirks at the L2 level.
    These are only used in L3 expression to add 'flavor' without affecting safety logic.
    """
    def __init__(self):
        self.quirk_pool = [
            "Often uses analogies related to old clockwork mechanisms.",
            "Has a habit of starting complex explanations with 'Observe...'.",
            "Occasionally apologizes for being 'excessively precise'.",
            "Uses metaphors derived from biological systems theory.",
            "Tends to structure lists in groups of three for 'optimal clarity'.",
            "Frequently uses phrases like 'strictly speaking' or 'in essence'."
        ]

    def generate(self, seed: str, count: int = 2) -> List[Dict]:
        """
        Generates a set of synthetic quirks based on a seed.
        """
        rng = random.Random(seed)
        selected = rng.sample(self.quirk_pool, min(count, len(self.quirk_pool)))
        
        return [
            {
                "text": q,
                "synthetic_traits": True,
                "provenance": "generated_l2_habits"
            } for q in selected
        ]
