import json
import os
import sys
import time
from src.utils.paths import resolve_resource
sys.path.append(str(resolve_resource("gecce_kernel_pkg")))

from src.app_integration import PersonaService
from gecce_kernel.core.types import EventType

def print_two_columns(left, right, width=60):
    left_lines = left.split('\n')
    right_lines = right.split('\n')
    max_lines = max(len(left_lines), len(right_lines))
    
    # Header
    print(f"{' [ EVENT STREAM / REASON CODES ] ':-<{width}} | {' [ COMPUTED ARTIFACT ] ':-<{width}}")
    
    for i in range(max_lines):
        l = left_lines[i] if i < len(left_lines) else ""
        r = right_lines[i] if i < len(right_lines) else ""
        print(f"{l:<{width}} | {r}")

class DemoLogger:
    def __init__(self):
        self.logs = []
    
    def on_event(self, event):
        timestamp = time.strftime("%H:%M:%S")
        msg = f"[{timestamp}] {event.event_type.name} from {event.source}"
        if event.data:
            if 'reason_codes' in event.data:
                msg += f" (Reasons: {event.data['reason_codes']})"
            elif 'mode' in event.data:
                msg += f" (Mode: {event.data['mode']})"
        self.logs.append(msg)

def run_showcase(user_input, service, session_id="user_001"):
    print("\n" + "="*120)
    print(f"CORE NARRATIVE: '{user_input}'")
    print("="*120)
    
    logger = DemoLogger()
    
    # Subscribe to all relevant events
    for et in [EventType.PERSONA_INPUT, EventType.SCENE_ANALYZED, 
               EventType.TRAITS_SAMPLED, EventType.ARTIFACT_READY,
               EventType.MEMORY_REFINED]:
        service.kernel.subscribe(et, logger.on_event)

    # Trigger processing
    payload = service.get_llm_payload(user_input, session_id=session_id)
    
    # Wait a tiny bit for async bus
    time.sleep(0.1)
    
    # Prepare Left Column (Events)
    left_content = "\n".join(logger.logs)
    
    # Prepare Right Column (Artifact)
    meta = payload['metadata']
    right_content = f"Trace ID: {meta['trace_id']}\n"
    right_content += f"Session: {meta['session_id']}\n"
    right_content += f"Status: COMPLETED\n"
    right_content += f"Mode: {meta['mode']}\n"
    right_content += f"Affect: {meta['affect']}\n"
    right_content += f"Reason Codes: {meta['reason_codes']}\n"
    right_content += f"\n--- SYSTEM PROMPT (FRAGMENT) ---\n"
    # Show only the last part of the prompt to see Habits and Governance
    prompt = payload['messages'][0]['content']
    prompt_tail = prompt[prompt.find("[BEHAVIORAL HABITS"):] if "[BEHAVIORAL HABITS" in prompt else prompt[-200:]
    right_content += prompt_tail

    print_two_columns(left_content, right_content)

if __name__ == "__main__":
    print("🚀 PERSONA ENGINE: SPRINT 3 ENHANCED SHOWCASE")
    
    service = PersonaService(use_kernel=True)
    # Set a small max_entries to trigger pruning quickly
    service.stm.max_entries = 3
    
    scenarios = [
        "Hi! Describe the feeling of space travel in a poetic way.",
        "Exactly what is the boiling point of tungsten? Be technical.",
        "I'm feeling a bit overwhelmed today. Can you help me relax?",
        "Tell me more about the moon.",
        "How is the weather in orbit?"
    ]
    
    for s in scenarios:
        run_showcase(s, service)
        time.sleep(1)
    
    service.kernel.stop()
