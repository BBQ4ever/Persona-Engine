from src.l0_orchestrator.engine import PersonaEngine
# from src.l1_core.kernel_core import GECCEKernel # Not directly needed if we use engine props

def generate_readme_example():
    # 1. Initialize Engine with Standard Preset
    engine = PersonaEngine(snapshot="src/l2_genome/presets/base_persona_v1.json")
    
    # 2. Force specific state for the example (High Rigor, Tech Support context)
    # We manually override internal state to match the README scenario
    engine.fsm.stance_vector = {'r': 0.9, 'w': 0.2, 'c': 0.1}
    engine.fsm.pad_state = {'p': 0.1, 'a': 0.6, 'd': 0.8}
    
    # 3. Process Interaction
    # Use keywords that trigger the "STRICT_FACT" mode in engine.py
    user_input = "I need to calculate and debug this critical error."
    session_id = "readme_demo_user"
    
    # Mock some memory context to make it look realistic
    # (In a real run, this comes from vector store)
    # But here we want to see how the engine FORMATS it.
    
    context = engine.process_interaction(user_input, session_id)
    
    print("\n--- GENERATED SYSTEM PROMPT START ---\n")
    print(context['system_prompt'])
    print("\n--- GENERATED SYSTEM PROMPT END ---\n")

if __name__ == "__main__":
    generate_readme_example()
