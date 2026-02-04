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
        
        # Scenario Category 1: Strict Fact/Logic (Auto-degrade)
        fact_keywords = [
            r"calculate", r"compute", r"prove", r"math", r"fact", 
            r"tutorial", r"critical", r"square root", r"formula", r"definition",
            r"sqrt", r"计算", r"证明", r"平方根", r"explain", r"theory", r"what is",
            r"python", r"function", r"sort", r"solve"
        ]
        for kw in fact_keywords:
            if re.search(kw, user_input):
                print(f"DEBUG: Matched keyword '{kw}'")
                return "STRICT_FACT"
                
        # Scenario Category 2: Social/Creative (Full Persona)
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
            effective_influence = 0.1  # Minimal personality to avoid interference
            mode = "STYLE_ONLY"
            print(f"📉 Scenario detected: {scene}. Degrading persona influence to {effective_influence}")
        else:
            effective_influence = self.influence_level
            mode = "FULL_PERSONA"
            print(f"📈 Scenario detected: {scene}. Influence level: {effective_influence}")
            
        return {
            "mode": mode,
            "influence": effective_influence,
            "genome_snapshot": self.genome,
            "persona_state": self.fsm.get_status()["state"]
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
