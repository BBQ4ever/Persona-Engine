from enum import Enum, auto
import time
from src.l1_core.affect import AffectiveManifold

class PersonaState(Enum):
    FORMING = auto()      # Initial creation, high flexibility
    STABILIZING = auto()  # Convergence phase
    STABLE = auto()       # Consistent persona
    DRIFTING = auto()     # Minor adjustments based on feedback
    LOCKED = auto()       # Hard consistency, no drift allowed

class PersonaFSM:
    def __init__(self, persona_id, initial_state=PersonaState.FORMING):
        self.persona_id = persona_id
        self.state = initial_state
        self.interaction_count = 0
        self.intimacy_level = 0.0  # Relationship depth [0.0 - 1.0]
        self.last_transition_time = time.time()
        self.history = []
        
        # Phase 8: Affective Substrate
        self.affect = AffectiveManifold()

    def transition_to(self, new_state):
        if self.state == PersonaState.LOCKED and new_state != PersonaState.LOCKED:
            print(f"⚠️ Warning: Attempted to unlock a LOCKED persona '{self.persona_id}'. Transition denied.")
            return False
        
        old_state = self.state
        self.state = new_state
        self.last_transition_time = time.time()
        self.history.append((old_state, new_state, self.interaction_count, self.last_transition_time))
        print(f"🔄 State Transition: {old_state.name} -> {new_state.name} (Interactions: {self.interaction_count})")
        return True

    def record_interaction(self, feedback_score=None):
        """
        Record an interaction and trigger automatic state transitions if needed.
        """
        self.interaction_count += 1
        
        # Simple automatic transition logic
        if self.state == PersonaState.FORMING and self.interaction_count >= 10:
            self.transition_to(PersonaState.STABILIZING)
        elif self.state == PersonaState.STABILIZING and self.interaction_count >= 50:
            self.transition_to(PersonaState.STABLE)
            
    def set_locked(self, locked=True):
        if locked:
            self.transition_to(PersonaState.LOCKED)
        else:
            # Only allow unlocking if we were previously in a state that allows it
            # For now, let's say transition from LOCKED to STABLE is allowed via explicit call
            self.state = PersonaState.STABLE
            print(f"🔓 Persona '{self.persona_id}' UNLOCKED -> STABLE")

    def get_status(self):
        return {
            "persona_id": self.persona_id,
            "state": self.state.name,
            "interaction_count": self.interaction_count,
            "intimacy_level": self.intimacy_level,
            "uptime": time.time() - self.last_transition_time,
            "affect": self.affect.get_affect()
        }

    def to_dict(self):
        return {
            "persona_id": self.persona_id,
            "state": self.state.name,
            "interaction_count": self.interaction_count,
            "intimacy_level": self.intimacy_level,
            "history": self.history,
            "affect": self.affect.to_dict()
        }

    def from_dict(self, data):
        self.persona_id = data.get("persona_id", self.persona_id)
        state_name = data.get("state", "FORMING")
        self.state = PersonaState[state_name]
        self.interaction_count = data.get("interaction_count", 0)
        self.intimacy_level = data.get("intimacy_level", 0.0)
        self.history = data.get("history", [])
        if "affect" in data:
            self.affect.from_dict(data["affect"])

if __name__ == "__main__":
    # Test the FSM
    fsm = PersonaFSM("test_ai")
    print(f"Initial Status: {fsm.get_status()}")
    
    # Simulate interactions
    for _ in range(12):
        fsm.record_interaction()
    
    print(f"Status after 12 interactions: {fsm.get_status()}")
    
    fsm.set_locked()
    fsm.transition_to(PersonaState.DRIFTING) # Should fail
    print(f"Final Status: {fsm.get_status()}")
