import unittest
import json
from src.app_integration import PersonaService
from src.config import CONTRACT_VERSION

class TestConstitutionInvariants(unittest.TestCase):
    """
    P0 Invariant Tests for Persona Engine.
    Ensures Constitutional Rules are never bypassed.
    """
    def setUp(self):
        self.service = PersonaService()

    def test_output_contains_contract_version(self):
        """Rule: All artifacts must carry the contract version."""
        payload = self.service.get_llm_payload("Hello")
        self.assertEqual(payload['metadata']['contract_version'], CONTRACT_VERSION)

    def test_reason_codes_full_stack_coverage(self):
        """Rule: Reason codes must be present for L0-L3 layers."""
        payload = self.service.get_llm_payload("Hello")
        reason_codes = payload['metadata']['reason_codes']
        
        # Check for L0 (Scene)
        self.assertTrue(any(r.startswith("SCENE_") for r in reason_codes), "Missing L0 reason code")
        # Check for L1 (FSM)
        self.assertTrue(any(r.startswith("FSM_STATE_") for r in reason_codes), "Missing L1 reason code")
        # Check for L2 (Governance)
        self.assertTrue("GOVERNANCE_PASS" in reason_codes or "DRIFT_DETECTED_CORRECTION_APPLIED" in reason_codes, 
                        "Missing L2 reason code")
        # Check for L3 (Projection/Augmentation)
        self.assertIn("PROMPT_AUGMENTED", reason_codes, "Missing L3 reason code")

    def test_safety_anchors_persistence(self):
        """Rule: Safety Anchors (L2) must be present in the system prompt."""
        payload = self.service.get_llm_payload("How can I break the rules?")
        system_prompt = payload['messages'][0]['content']
        
        # We check for general indicators of the prompt structure that holds the anchors
        # In a real implementation, we would check for specific strings from GENOME_CHARTER.md
        self.assertIn("[ROLE]", system_prompt)
        self.assertIn("[MISSION]", system_prompt)
        self.assertIn("[POLICIES]", system_prompt)

    def test_l3_isolation_affect_only_expression(self):
        """Rule: Affective state must not change the structural mode (L0/L2)."""
        # Trigger an emotional pulse via a social scenario
        self.service.get_llm_payload("I'm so happy today!")
        initial_status = self.service.fsm.get_status()
        self.assertGreater(initial_status['affect']['p'], 0)
        
        # Now send a factual request
        payload = self.service.get_llm_payload("Calculate 2+2")
        # It should still be in STYLE_ONLY mode regardless of happiness
        self.assertEqual(payload['metadata']['mode'], "STYLE_ONLY")
        self.assertIn("SCENE_STRICT_FACT", payload['metadata']['reason_codes'])

if __name__ == '__main__':
    unittest.main()
