import sys
import os
import json
import time

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from kernel_integration import PersonaKernel
from l0_orchestrator.kernel_orchestrator import KernelOrchestrator
from l1_core.kernel_core import KernelCore
from l3_expression.kernel_expression import KernelExpression
from gecce_kernel.core.types import Event, EventType

def main():
    print("\n" + "🏮 Persona Engine: Kernel-Driven Mode (Powered by GECCE)" + "\n")
    
    # 1. Initialize Kernel Substrate
    kernel = PersonaKernel()
    
    # 2. Load Genome
    with open("src/l2_genome/sample_genome.json", "r") as f:
        genome = json.load(f)
        
    # 3. Initialize Kernel Modules
    l0 = KernelOrchestrator(kernel.bus, name="L0-Orchestrator")
    l1 = KernelCore(kernel.bus, persona_id="pioneer_v2", name="L1-Core")
    l3 = KernelExpression(kernel.bus, genome_data=genome, name="L3-Expression")
    
    # Register them so the kernel knows about them
    from gecce_kernel.core.types import ModuleType
    kernel.registry.register("L0-Orchestrator", ModuleType.VALIDATION, l0)
    kernel.registry.register("L1-Core", ModuleType.FEATURE_MODULE, l1)
    kernel.registry.register("L3-Expression", ModuleType.RENDERING, l3)
    
    # 4. Setup a listener for the final projection (Mocking the UI/LLM consumption)
    def on_final_projection(event: Event):
        print(f"\n[FINAL OUTPUT] Event ID: {event.event_id}")
        print(f"  - Influence: {event.data['influence']}")
        print(f"  - Projection: {event.data['projection']}")
        
    kernel.subscribe(EventType.PERSONA_PROJECTION, on_final_projection)
    
    # 5. Simulate interactions
    print("\n>>> Scenario A: Regular Chat")
    kernel.publish_event(EventType.PERSONA_INPUT, "UserConnector", {
        "text": "Tell me a joke about robots!",
        "session_id": "session_A"
    })
    time.sleep(1) # Wait for async processing
    
    print("\n>>> Scenario B: Strict Calculation")
    kernel.publish_event(EventType.PERSONA_INPUT, "UserConnector", {
        "text": "What is the square root of 256?",
        "session_id": "session_B"
    })
    time.sleep(1)
    
    # --- New: Snapshot Capture ---
    print("\n>>> Capturing System Snapshot...")
    kernel.take_snapshot(label="end_of_demo")
    
    # Cleanup
    kernel.stop()
    print("\n✅ Kernel demo completed.")

if __name__ == "__main__":
    main()
