import json
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from l0_orchestrator.engine import PersonaEngine
from l1_core.fsm import PersonaFSM, PersonaState
from l3_expression.projection import SeededSampler

def run_persona_pipeline(user_input, session_id="user_001"):
    print(f"\n" + "="*50)
    print(f"USER INPUT: '{user_input}'")
    print("="*50)
    
    # 1. Load Genome (L2)
    genome_path = "src/l2_genome/sample_genome.json"
    if not os.path.exists(genome_path):
        # Fallback for different working directories
        genome_path = "l2_genome/sample_genome.json"
        
    with open(genome_path, "r") as f:
        genome = json.load(f)
        
    # 2. Setup Systems (L1 & L0)
    fsm = PersonaFSM("pioneer_v1", initial_state=PersonaState.STABLE)
    engine = PersonaEngine(fsm, genome)
    sampler = SeededSampler()
    
    # 3. L0: Get Influence and Constraints
    constraints = engine.get_effective_constraints(user_input)
    
    if not constraints:
        print("System operating in Basic Mode.")
        return
        
    # 4. L3: Sample specific trait values for this expression
    print("\n--- L3 Projection Results ---")
    active_traits = {}
    for trait in genome['loci']:
        sampled = sampler.sample_trait(trait, session_id, influence=constraints['influence'])
        active_traits[trait['id']] = sampled
        print(f"Trait '{trait['id']}': {sampled if isinstance(sampled, str) else format(sampled, '.3f')}")
    
    # 5. Resulting Narrative Context (Mocking the Prompt for LLM)
    print("\n--- Generated Prompt Context (Internal) ---")
    mode_desc = "Be yourself and express your personality." if constraints['mode'] == "FULL_PERSONA" else "Be concise and factual."
    print(f"Instruction: {mode_desc}")
    print(f"Stance: {active_traits.get('conflict_strategy', 'analytical')}")
    print(f"Tone: {'Humorous' if active_traits.get('humor_density', 0) > 0.3 else 'Professional'}")

if __name__ == "__main__":
    # Test cases representing different scenarios
    run_persona_pipeline("Hi there! Tell me something interesting about space.")
    run_persona_pipeline("What is the exact square root of 144?")
    run_persona_pipeline("I disagree with your previous statement. Prove it.")
