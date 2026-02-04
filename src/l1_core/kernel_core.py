import sys
import os

# Add path for gecce_kernel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "gecce_kernel_pkg")))

from gecce_kernel.core.types import Event, EventType
from gecce_kernel.core.modules.base_module import ModuleContext, ModuleResult
from kernel_integration import PersonaBaseModule
from .fsm import PersonaState

class KernelCore(PersonaBaseModule):
    """
    L1 Core - 内核化版本
    职责：管理状态，监听交互增加计数。
    """
    def __init__(self, bus, persona_id, **kwargs):
        super().__init__(bus, **kwargs)
        self.persona_id = persona_id
        self.state = PersonaState.FORMING
        self.interaction_count = 0
        
        # 订阅输入事件以自动演化
        self.bus.subscribe(EventType.PERSONA_INPUT, self.on_interaction)

    def on_interaction(self, event: Event):
        self.interaction_count += 1
        old_state = self.state
        
        # 演变逻辑
        if self.state == PersonaState.FORMING and self.interaction_count >= 10:
            self.state = PersonaState.STABILIZING
        elif self.state == PersonaState.STABILIZING and self.interaction_count >= 50:
            self.state = PersonaState.STABLE
            
        if old_state != self.state:
            self.notify_event(EventType.PERSONA_STATE_CHANGED, {
                "persona_id": self.persona_id,
                "old_state": old_state.name,
                "new_state": self.state.name,
                "interaction_count": self.interaction_count
            })

    def capture_state(self) -> dict:
        return {
            "state": self.state.name,
            "interaction_count": self.interaction_count,
            "persona_id": self.persona_id
        }

    def process(self, context: ModuleContext) -> ModuleResult:
        result = ModuleResult()
        result.metrics['state'] = self.state.name
        result.metrics['interaction_count'] = self.interaction_count
        return result
