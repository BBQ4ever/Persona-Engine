import unittest
import json
from src.app_integration import PersonaService

class TestDirectorEquivalence(unittest.TestCase):
    """
    Verifies that the new CognitiveDirector produces results equivalent 
    to the baseline expectations of the Persona Engine.
    """
    def setUp(self):
        self.service = PersonaService()

    def test_social_scenario_equivalence(self):
        """Verify social scenario produces FULL_PERSONA mode and supportive metadata."""
        payload = self.service.get_llm_payload("I need some help feeling better.")
        
        self.assertEqual(payload['metadata']['mode'], "FULL_PERSONA")
        self.assertIn("SCENE_SOCIAL_SUPPORT", payload['metadata']['reason_codes'])
        self.assertEqual(payload['metadata']['stance']['warmth'], 0.9)

    def test_strict_fact_scenario_equivalence(self):
        """Verify factual scenario produces STYLE_ONLY mode and high rigor."""
        payload = self.service.get_llm_payload("Calculate the speed of light in a vacuum.")
        
        self.assertEqual(payload['metadata']['mode'], "STYLE_ONLY")
        self.assertIn("SCENE_STRICT_FACT", payload['metadata']['reason_codes'])
        self.assertEqual(payload['metadata']['stance']['rigor'], 0.9)

if __name__ == '__main__':
    unittest.main()
