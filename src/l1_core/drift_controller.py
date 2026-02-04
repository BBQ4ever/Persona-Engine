import json
import copy

class DriftController:
    def __init__(self, variability_multiplier=0.1):
        self.variability_multiplier = variability_multiplier

    def apply_drift(self, genome, feedback_vector):
        """
        Applies drift to genome traits based on feedback and trait variability.
        feedback_vector: dict mapping trait_id to a delta value (-1 to 1)
        """
        drifted_genome = copy.deepcopy(genome)
        
        for locus in drifted_genome.get('loci', []):
            locus_id = locus['id']
            if locus_id in feedback_vector:
                feedback = feedback_vector[locus_id]
                variability = locus.get('variability', 0.5)
                
                # Apply drift to distribution parameters
                dist = locus['distribution']
                if dist['type'] == 'range':
                    current_default = dist['values']['default']
                    # Calculate delta: feedback * variability * some global factor
                    delta = feedback * variability * self.variability_multiplier
                    
                    new_default = current_default + delta
                    
                    # Clamp to min/max
                    min_val = dist['values']['min']
                    max_val = dist['values']['max']
                    new_default = max(min_val, min(max_val, new_default))
                    
                    dist['values']['default'] = round(new_default, 4)
                    print(f"🌊 Drifting '{locus_id}': {current_default} -> {dist['values']['default']} (Var: {variability})")
        
        return drifted_genome

if __name__ == "__main__":
    # Test Drift
    with open("src/l2_genome/sample_genome.json", "r") as f:
        sample = json.load(f)
        
    dc = DriftController()
    
    # User feedback: "Too simple, give more abstract explanations" (+ feedback for explanation_depth)
    # "Stop joking so much" (- feedback for humor_density)
    feedback = {
        "explanation_depth": 0.5,
        "humor_density": -0.8
    }
    
    print("Pre-drift explanation_depth:", sample['loci'][0]['distribution']['values']['default'])
    
    drifted = dc.apply_drift(sample, feedback)
    
    print("Post-drift explanation_depth:", drifted['loci'][0]['distribution']['values']['default'])
