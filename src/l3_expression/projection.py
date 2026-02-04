import random
import hashlib

class SeededSampler:
    def __init__(self, time_bucket_size=3600):
        self.time_bucket_size = time_bucket_size

    def _get_seed(self, session_id, time_seed=None):
        if time_seed is None:
            # Create a time bucket (e.g., changes every hour for "long term variance")
            import time
            time_seed = int(time.time() / self.time_bucket_size)
        
        seed_str = f"{session_id}_{time_seed}"
        return int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)

    def sample_trait(self, trait_locus, session_id, influence=1.0, affect_warp=None):
        """
        Sample a value from the locus distribution using a stable seed.
        """
        if affect_warp is None:
            affect_warp = {"variability_warp": 1.0, "bias_warp": 0.0}

        seed = self._get_seed(session_id)
        rng = random.Random(seed)
        
        dist = trait_locus['distribution']
        base_value = 0.5
        
        if dist['type'] == 'range':
            vals = dist['values']
            # Stochastic value within range
            stochastic_val = rng.uniform(vals['min'], vals['max'])
            # Shift towards default based on influence (1.0 = full stochastic within drift, 
            # 0.0 = stick strictly to default or neutral 0.5)
            # Actually, standard interpretation: influence scales the range or anchors to mean
            default = vals['default']
            
            # Phase 8: Apply Affective Warp
            # Arousal expands the variability
            effective_variability = trait_locus.get('variability', 0.1) * affect_warp['variability_warp']
            
            # Dominance/Pleasure can bias the default (not fully implemented yet, but keeping structure)
            effective_default = max(vals['min'], min(vals['max'], default + affect_warp['bias_warp']))
            
            # Apply influence: control how much we drift from the default toward a stochastic point
            # Lower influence/variability keeps us anchored to the default (Stance)
            drift_amount = (stochastic_val - effective_default) * influence * effective_variability
            base_value = effective_default + drift_amount
            base_value = max(vals['min'], min(vals['max'], base_value))
            
        elif dist['type'] == 'categorical':
            choices = list(dist['values'].keys())
            weights = list(dist['values'].values())
            # Simple weighted choice
            base_value = rng.choices(choices, weights=weights, k=1)[0]
            
        return base_value

if __name__ == "__main__":
    # Test L3 Projection
    import json
    with open("src/l2_genome/sample_genome.json", "r") as f:
        genome = json.load(f)
        
    sampler = SeededSampler()
    
    trait = genome['loci'][0] # explanation_depth
    print(f"Sampling for {trait['id']}...")
    
    # Test stability: same session should yield same value
    val1 = sampler.sample_trait(trait, "session_42")
    val2 = sampler.sample_trait(trait, "session_42")
    print(f"Val 1: {val1:.4f}, Val 2 (same session): {val2:.4f}")
    
    # Test variance: different session should yield different value
    val3 = sampler.sample_trait(trait, "session_99")
    print(f"Val 3 (different session): {val3:.4f}")
    
    # Test influence: low influence should draw closer to default (0.35)
    val_low = sampler.sample_trait(trait, "session_99", influence=0.1)
    print(f"Val Low Influence (0.1): {val_low:.4f} (Default: 0.35)")
