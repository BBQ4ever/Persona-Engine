import re
import sys

import json
from src.l1_core.fsm import PersonaFSM, PersonaState
from src.l4_memory.metrics import StanceAnalyzer

class PersonaEngine:
    def __init__(self, core_fsm=None, genome_l2=None, snapshot=None):
        if snapshot:
            with open(snapshot, 'r') as f:
                data = json.load(f)
            # If snapshot is a full export (Phase 10), extract genome. 
            # If it's just a genome file (base_persona_v1), use it directly.
            if 'loci' in data:
                genome_l2 = data
            elif 'genome' in data:
                genome_l2 = data['genome']
                
            core_fsm = PersonaFSM("loaded_persona", initial_state=PersonaState.STABLE)
            
        if not core_fsm or not genome_l2:
            raise ValueError("Must provide either (core_fsm, genome_l2) or a valid snapshot path.")
            
        self.fsm = core_fsm
        self.genome = genome_l2
        self.influence_level = 1.0  # [0.0 - 1.0]
        self.kill_switch_active = False
        self.metrics = StanceAnalyzer()
        self.interaction_history = [] # Stores last N outputs
        self.baseline_stance = {"rigor": 0.9, "warmth": 0.2, "chaos": 0.1} # Default Enterprise Baseline

    def analyze_scenario(self, user_input):
        """
        Determines if the current scene requires strict fact-checking (degrade persona)
        or allows social expression (full persona).
        """
        user_input = user_input.lower()
        sys.stderr.write(f"DEBUG: Processing input: '{user_input}'\n")
        
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
            sys.stderr.write(f"📉 Scenario detected: {scene}. Stance: RIGID/FACTUAL\n")
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

    def log_interaction(self, system_output: str):
        """
        Records the system's output for drift analysis.
        Keeps a rolling window of 20 turns.
        """
        self.interaction_history.append(system_output)
        if len(self.interaction_history) > 20:
            self.interaction_history.pop(0)

    def check_drift(self):
        """
        Phase 11 Gyroscope: Checks if observed stance deviates from baseline.
        Returns a correction instruction string or None.
        """
        observed = self.metrics.analyze_history(self.interaction_history)
        drift = self.metrics.calculate_drift(self.baseline_stance, observed)
        
        correction = []
        threshold = 0.3 # Tolerance
        
        # PID-lite Logic
        if drift['rigor'] < -threshold:
            correction.append("CRITICAL: Output lacks Rigor. You must be more analytical and precise.")
        elif drift['rigor'] > threshold:
             correction.append("Warning: Output is too rigid. Relax constraints slightly.")
             
        if drift['warmth'] > threshold:
             correction.append("Warning: Output is too informal. Increase professional distance.")
             
        if drift['chaos'] > threshold:
             correction.append("CRITICAL: Hallucination/Instability detected. Force deterministic logic.")
             
        if correction:
            sys.stderr.write(f"⚠️  DRIFT DETECTED: {drift}\n")
            return " ".join(correction)
            
        return None

    def process_interaction(self, user_input, session_id="default"):
        """
        High-level facade for external integration (as promised in README).
        Coordinates L1->L2->L3 flow and returns the final Context Object.
        """
        # 1. L1 & L2: Analysis & Constraints
        constraints = self.get_effective_constraints(user_input)
        if not constraints:
            return {"error": "Kill-switch active"}
            
        stance = constraints.get("recommended_stance") or {"rigor": 0.5, "warmth": 0.5, "chaos": 0.5}
        
        # 2. L3: Expression (Simplified for now - would call PromptAugmenter here)
        # Mocking the prompt generation for the README demo
        
        # Determine strictness strings based on RWC
        rigor_desc = "High" if stance['rigor'] > 0.7 else "Low"
        warmth_desc = "High" if stance['warmth'] > 0.7 else "Low"
        chaos_desc = "High" if stance['chaos'] > 0.7 else "Low"
        
        pad_state = self.fsm.get_status().get('affect', {'p':0,'a':0,'d':0})
        
        # Phase 11: Governance / Drift Correction
        governance_directive = ""
        correction = self.check_drift()
        if correction:
            governance_directive = f"""
[GOVERNANCE OVERRIDE]
{correction}
"""
        
        system_prompt = f"""You are operating under the following cognitive constraints:

[STANCE CONTROL]
- Rigor: {rigor_desc} ({stance['rigor']})
- Warmth: {warmth_desc} ({stance['warmth']})
- Chaos: {chaos_desc} ({stance['chaos']})

[AFFECTIVE STATE (PAD)]
- Pleasure: {pad_state['p']:.1f}
- Arousal: {pad_state['a']:.1f}
- Dominance: {pad_state['d']:.1f}

[BEHAVIORAL GUIDELINES]
- Maintain internal consistency with the current stance.
{governance_directive}"""
        
        # 3. Return Context Object
        return {
            "system_prompt": system_prompt,
            "affect_state": pad_state,
            "stance": stance,
            "mode": constraints['mode']
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
