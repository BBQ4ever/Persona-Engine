import json
import copy
import os

class ArchetypeManager:
    """
    Fluid Stance Manager (R.W.C Model)
    Translates high-level stance vectors (Rigor, Warmth, Chaos) into low-level DNA.
    """
    def __init__(self, base_genome, config_path="src/l2_genome/presets/standard_archetypes.json"):
        self.base_genome = base_genome
        self.presets = {}
        
        # Load presets if available
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.presets = json.load(f).get("presets", {})

    def get_preset_stance(self, preset_name):
        return self.presets.get(preset_name, {"rigor": 0.5, "warmth": 0.5, "chaos": 0.3})

    def calculate_genome_from_stance(self, rigor: float, warmth: float, chaos: float):
        """
        The core mapping algorithm: Maps 3D stance to multi-dimensional DNA space.
        rigor: [0.0 - 1.0] -> logical depth, rigor, analytical strategy
        warmth: [0.0 - 1.0] -> happiness baseline, feminine bias, harmony strategy
        chaos: [0.0 - 1.0] -> humor, trait variability, stochastic jitter
        """
        new_genome = copy.deepcopy(self.base_genome)
        
        # Constraints clipping
        r = max(0.0, min(1.0, rigor))
        w = max(0.0, min(1.0, warmth))
        c = max(0.0, min(1.0, chaos))

        for locus in new_genome['loci']:
            l_id = locus['id']
            vals = locus['distribution']['values']
            
            # 1. Map Rigor (R)
            if l_id == "logical_rigor":
                # Scale between min and max based on R
                locus['distribution']['values']['default'] = vals['min'] + (vals['max'] - vals['min']) * r
            elif l_id == "explanation_depth":
                 locus['distribution']['values']['default'] = vals['min'] + (vals['max'] - vals['min']) * r

            # 2. Map Warmth (W)
            elif l_id == "identity_signature":
                # W=1.0 is full Warm/Feminine, W=0.0 is cold/masculine
                locus['distribution']['values']['default'] = w
            
            # 3. Map Chaos (C)
            elif l_id == "humor_density":
                locus['distribution']['values']['default'] = vals['min'] + (vals['max'] - vals['min']) * c
            
            # 4. Global Effects of Chaos (C) on Variability
            # Higher chaos means higher stochastic noise for all traits
            locus['variability'] = 0.05 + (0.4 * c)

            # 5. Categorical Mappings (Conflict Strategy)
            if l_id == "conflict_strategy":
                # Distribute probabilities based on R and W
                # analytical (favored by R), accommodating (favored by W), assertive (neutral)
                total = r + w + 0.3 # 0.3 is base for assertive
                locus['distribution']['values'] = {
                    "analytical": round(r / total, 2),
                    "accommodating": round(w / total, 2),
                    "assertive": round(0.3 / total, 2)
                }

        return new_genome

    def get_affect_baseline(self, rigor, warmth, chaos):
        """
        Derive emotional baseline from stance.
        """
        return {
            "p": round((warmth * 0.8) - 0.2, 3), # High warmth -> High Pleasure
            "a": round((chaos * 0.7) - 0.1, 3),  # High chaos -> High Arousal
            "d": round((rigor * 0.6) - 0.1, 3)   # High rigor -> High Dominance
        }
