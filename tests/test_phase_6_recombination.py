import unittest
import json
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.l1_core.recombinator import GenomeRecombinator

class TestPhase6Recombination(unittest.TestCase):
    
    def setUp(self):
        # Create dummy parent genomes
        self.parent_a = {
            "version": "1.0",
            "metadata": {"persona_id": "parent_a"},
            "loci": [
                {
                    "id": "humor_density",
                    "category": "style",
                    "distribution": {
                        "type": "range",
                        "values": {"min": 0.0, "max": 1.0, "default": 0.2}
                    }
                },
                {
                    "id": "truth_alignment", # Safety anchor
                    "category": "value",
                    "distribution": {
                        "type": "range",
                        "values": {"min": 0.9, "max": 1.0, "default": 1.0}
                    }
                }
            ]
        }
        
        self.parent_b = {
            "version": "1.0",
            "metadata": {"persona_id": "parent_b"},
            "loci": [
                {
                    "id": "humor_density",
                    "category": "style",
                    "distribution": {
                        "type": "range",
                        "values": {"min": 0.0, "max": 1.0, "default": 0.8}
                    }
                },
                {
                    "id": "truth_alignment",
                    "category": "value",
                    "distribution": {
                        "type": "range",
                        "values": {"min": 0.9, "max": 1.0, "default": 1.0}
                    }
                }
            ]
        }
        
        self.recombinator = GenomeRecombinator(mutation_rate=0.0) # Zero mutation for deterministic testing

    def test_crossover_averaging(self):
        """Test that scalar traits are averaged between parents."""
        child = self.recombinator.recombine(self.parent_a, self.parent_b, "child_test")
        
        # Find humor_density
        humor = next(l for l in child['loci'] if l['id'] == 'humor_density')
        
        # Parent A: 0.2, Parent B: 0.8 -> Expected Child: 0.5
        self.assertAlmostEqual(humor['distribution']['values']['default'], 0.5)

    def test_safety_anchors_immutability(self):
        """Test that safety anchors are not mutated."""
        # Enable high mutation rate
        self.recombinator.mutation_rate = 1.0
        
        child = self.recombinator.recombine(self.parent_a, self.parent_b, "child_test")
        
        # Find truth_alignment
        truth = next(l for l in child['loci'] if l['id'] == 'truth_alignment')
        
        # Should remain exactly 1.0 (Average of 1.0 and 1.0 is 1.0, and mutation should be skipped)
        self.assertEqual(truth['distribution']['values']['default'], 1.0)
        
    def test_mutation_drift(self):
        """Test that non-anchor traits drift when mutation is enabled."""
        self.recombinator.mutation_rate = 1.0
        
        # Run multiple times to catch stochastic drift (since drift is random +/-)
        # We just need to ensure it's NOT exactly 0.5 (the average)
        drift_detected = False
        for _ in range(10):
            child = self.recombinator.recombine(self.parent_a, self.parent_b, "child_test")
            humor = next(l for l in child['loci'] if l['id'] == 'humor_density')
            if abs(humor['distribution']['values']['default'] - 0.5) > 0.0001:
                drift_detected = True
                break
                
        self.assertTrue(drift_detected, "Mutation should cause drift from the perfect average")

    def test_metadata_lineage(self):
        """Test that parent lineage is recorded."""
        child = self.recombinator.recombine(self.parent_a, self.parent_b, "child_test")
        
        parents = child['metadata']['parents']
        self.assertIn("parent_a", parents)
        self.assertIn("parent_b", parents)

if __name__ == '__main__':
    unittest.main()
