import time

class AffectiveManifold:
    """
    Implementation of the PAD (Pleasure, Arousal, Dominance) Emotional Model.
    This manages the short-term emotional flux of the persona.
    """
    def __init__(self, baseline_p=0.0, baseline_a=0.0, baseline_d=0.0):
        # Current PAD state values regulated within [-1.0, 1.0]
        self.p = baseline_p  # Pleasure: Valence (Happy vs Sad)
        self.a = baseline_a  # Arousal: Activation (Excited vs Calm)
        self.d = baseline_d  # Dominance: Assertiveness (Confident vs Submissive)
        
        # Baselines (Personality defaults derived from L2)
        self.baseline = {'p': baseline_p, 'a': baseline_a, 'd': baseline_d}
        
        # Decay rates (percentage per step to return to baseline)
        self.decay_rate = 0.1
        self.last_update = time.time()

    def set_baseline(self, p=None, a=None, d=None):
        if p is not None: self.baseline['p'] = p
        if a is not None: self.baseline['a'] = a
        if d is not None: self.baseline['d'] = d
        # Optionally snap to baseline immediately
        self.p = self.baseline['p']
        self.a = self.baseline['a']
        self.d = self.baseline['d']

    def update(self, delta_p=0.0, delta_a=0.0, delta_d=0.0):
        """
        Inject an emotional pulse (e.g., from L0 sentiment analysis).
        """
        self.p = max(-1.0, min(1.0, self.p + delta_p))
        self.a = max(-1.0, min(1.0, self.a + delta_a))
        self.d = max(-1.0, min(1.0, self.d + delta_d))
        self.last_update = time.time()

    def decay(self):
        """
        Naturally decay toward baseline over time.
        """
        self.p += (self.baseline['p'] - self.p) * self.decay_rate
        self.a += (self.baseline['a'] - self.a) * self.decay_rate
        self.d += (self.baseline['d'] - self.d) * self.decay_rate

    def get_affect(self):
        return {
            "p": round(self.p, 3),
            "a": round(self.a, 3),
            "d": round(self.d, 3)
        }

    def get_warp_factors(self):
        """
        Calculate how the current mood should wrap the L3 sampling.
        Returns multipliers for variance and bias.
        """
        # Example logic: High Arousal increases variability
        variability_warp = 1.0 + (abs(self.a) * 0.5)
        
        # High Dominance shifts assertive/logic traits upward
        bias_warp = self.d * 0.2
        
        return {
            "variability_warp": variability_warp,
            "bias_warp": bias_warp
        }

if __name__ == "__main__":
    # Test
    am = AffectiveManifold()
    print(f"Initial Affect: {am.get_affect()}")
    
    # Simulate a happy, exciting event
    am.update(delta_p=0.6, delta_a=0.4, delta_d=0.2)
    print(f"After Event: {am.get_affect()}")
    print(f"Warp Factors: {am.get_warp_factors()}")
    
    # Simulate decay
    for i in range(5):
        am.decay()
        print(f"Decay Step {i+1}: {am.get_affect()}")
