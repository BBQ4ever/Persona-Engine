import re

class StanceAnalyzer:
    """
    Phase 11: Metrics Extraction System (The Yardstick).
    Analyzes interaction history to determine theoretical R.W.C values (Observed Stance).
    """
    
    def __init__(self):
        # Heuristic keywords for lightweight analysis
        self.warmth_markers = [
            "sorry", "happy", "love", "feel", "great", "please", "thanks", "friend", "support",
            "😊", "❤️", "👍", "appreciate"
        ]
        self.rigor_markers = [
            "therefore", "because", "calculate", "logic", "proof", "step-by-step", "analysis",
            "statistically", "evidence", "fact", "1", "2", "3"
        ]
        self.chaos_markers = [
             "maybe", "perhaps", "weird", "random", "dream", "imagine", "wild", "matrix",
             "cyber", "entropy", "chaos"
        ]

    def analyze_history(self, history_entries):
        """
        Analyzes a list of user/assistant interaction texts.
        Returns a dict: {'rigor': 0.0-1.0, 'warmth': 0.0-1.0, 'chaos': 0.0-1.0}
        """
        if not history_entries:
            # Return neutral if no history
            return {'rigor': 0.5, 'warmth': 0.5, 'chaos': 0.5}

        # Combine text for analysis (focusing on Assistant output implies we need logs of Assisant output)
        # For now, we assume history_entries contains text strings of the Persona's Output
        combined_text = " ".join([str(e) for e in history_entries]).lower()
        total_words = len(combined_text.split())
        if total_words == 0:
             return {'rigor': 0.5, 'warmth': 0.5, 'chaos': 0.5}

        # Calculate density
        w_count = sum(1 for w in self.warmth_markers if w in combined_text)
        r_count = sum(1 for w in self.rigor_markers if w in combined_text)
        c_count = sum(1 for w in self.chaos_markers if w in combined_text)

        # Normalize (Arbitrary scaling for demo purposes)
        # A density of 1 marker per 20 words is considered "High"
        def normalize(count, total):
            density = count / max(total, 1)
            val = min(density * 20, 1.0) # Scaling factor
            return float(f"{val:.2f}")

        return {
            'rigor': normalize(r_count, total_words),
            'warmth': normalize(w_count, total_words),
            'chaos': normalize(c_count, total_words)
        }

    def calculate_drift(self, target_stance, observed_stance):
        """
        Calculates the delta between Target (Genome) and Observed (Behavior).
        """
        delta = {
            'rigor': observed_stance['rigor'] - target_stance['rigor'],
            'warmth': observed_stance['warmth'] - target_stance['warmth'],
            'chaos': observed_stance['chaos'] - target_stance['chaos']
        }
        # Formatting for readability
        return {k: float(f"{v:.2f}") for k, v in delta.items()}
