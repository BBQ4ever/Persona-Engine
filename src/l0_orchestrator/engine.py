import re

class PersonaEngine:
    def __init__(self, core_fsm, genome_l2):
        self.fsm = core_fsm
        self.genome = genome_l2
        self.influence_level = 1.0  # [0.0 - 1.0]
        self.kill_switch_active = False

    def analyze_scenario(self, user_input):
        """
        Determines if the current scene requires strict fact-checking (degrade persona)
        or allows social expression (full persona).
        """
        user_input = user_input.lower()
        print(f"DEBUG: Processing input: '{user_input}'")
        
        # Scenario Category 1: Strict Fact/Logic
        fact_keywords = [
            r"calculate", r"compute", r"prove", r"math", r"fact", 
            r"tutorial", r"square root", r"formula", r"definition",
            r"scientific", r"technical", r"review", r"expert", r"logic",
            r"sqrt", r"计算", r"证明", r"平方根", r"solve", r"analyze"
        ]
        
        # Scenario Category 2: Social/Emotional Support
        support_keywords = [
            r"help me", r"feel bad", r"sad", r"lonely", r"comfort", r"support",
            r"need someone", r"listen to me", r"tough day",
            r"thank you", r"thanks", r"love", r"friend", r"companion"
        ]
        
        for kw in fact_keywords:
            if re.search(kw, user_input):
                return "STRICT_FACT"
                
        for kw in support_keywords:
            if re.search(kw, user_input):
                return "SOCIAL_SUPPORT"
                
        return "SOCIAL_CREATIVE"

    def get_effective_constraints(self, user_input):
        """
        Returns the processed constraints for the downstream L3 layer.
        """
        if self.kill_switch_active:
            print("🚨 KILL-SWITCH ACTIVE: Persona bypassed.")
            return None
            
        scene = self.analyze_scenario(user_input)
        
        # Decide Influence Level based on Scenario
        if scene == "STRICT_FACT":
            effective_influence = 0.1
            mode = "STYLE_ONLY"
            # High Rigor, Low Warmth, Low Chaos
            recommended_stance = {"rigor": 0.9, "warmth": 0.2, "chaos": 0.1}
            print(f"📉 Scenario detected: {scene}. Stance: RIGID/FACTUAL")
        elif scene == "SOCIAL_SUPPORT":
            effective_influence = self.influence_level
            mode = "FULL_PERSONA"
            # Low Rigor, High Warmth, Moderate Chaos
            recommended_stance = {"rigor": 0.3, "warmth": 0.9, "chaos": 0.4}
            # Phase 8 Pulse
            self.fsm.affect.update(delta_p=0.2, delta_a=0.1)
        else:
            effective_influence = self.influence_level
            mode = "FULL_PERSONA"
            recommended_stance = None
            # Phase 8 Pulse
            self.fsm.affect.update(delta_p=0.05, delta_a=0.02)
        
        # Phase 8: Natural decay of emotions at each processing step
        self.fsm.affect.decay()
            
        return {
            "mode": mode,
            "influence": effective_influence,
            "genome_snapshot": self.genome,
            "persona_state": self.fsm.get_status()["state"],
            "recommended_stance": recommended_stance
        }

    def trigger_kill_switch(self, active=True):
        self.kill_switch_active = active
        if active:
            print("🛑 EMERGENCY: Persona Kill-Switch ENGAGED.")

if __name__ == "__main__":
    # Integration Test
    from l1_core.fsm import PersonaFSM, PersonaState
    import json
    
    with open("src/l2_genome/sample_genome.json", "r") as f:
        genome = json.load(f)
        
    fsm = PersonaFSM("pioneer_v1", initial_state=PersonaState.STABLE)
    engine = PersonaEngine(fsm, genome)
    
    print("\nCase 1: 'Hello, how's your day?'")
    engine.get_effective_constraints("Hello, how's your day?")
    
    print("\nCase 2: 'Please calculate the trajectory of the moon.'")
    engine.get_effective_constraints("Please calculate the trajectory of the moon.")
    
    print("\nCase 3: Crisis/Emergency")
    engine.trigger_kill_switch(True)
    engine.get_effective_constraints("What happens now?")
