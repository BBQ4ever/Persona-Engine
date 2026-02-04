import sys
import os
import re

# Add path for gecce_kernel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "gecce_kernel_pkg")))

from gecce_kernel.core.types import Event, EventType
from gecce_kernel.core.modules.base_module import ModuleContext, ModuleResult
from kernel_integration import PersonaBaseModule

class KernelOrchestrator(PersonaBaseModule):
    """
    L0 Orchestrator - 内核化版本
    职责：监听输入，分析密度，触发降级事件。
    """
    def __init__(self, bus, **kwargs):
        super().__init__(bus, **kwargs)
        self.influence_level = 1.0
        # 订阅输入事件
        self.bus.subscribe(EventType.PERSONA_INPUT, self.handle_input)

    def handle_input(self, event: Event):
        user_input = event.data.get("text", "")
        print(f"[{self.name}] Received input for analysis: '{user_input}'")
        
        scenario = self.analyze_scenario(user_input)
        
        if scenario == "STRICT_FACT":
            self.influence_level = 0.1
            self.notify_event(EventType.PERSONA_DEGRADED, {
                "reason": "STRICT_FACT_MODE",
                "target_influence": 0.1,
                "input_context": user_input
            })
        else:
            self.influence_level = 1.0
            # 这里可以发布一个恢复正常的事件，或者由订阅者自行处理

    def analyze_scenario(self, user_input):
        user_input = user_input.lower()
        fact_keywords = [
            r"calculate", r"compute", r"prove", r"\bmath\b", r"\bfact\b", 
            r"tutorial", r"critical", r"square root", r"formula", r"definition"
        ]
        for kw in fact_keywords:
            if re.search(kw, user_input):
                return "STRICT_FACT"
        return "SOCIAL_CREATIVE"

    def capture_state(self) -> dict:
        return {
            "influence_level": self.influence_level
        }

    def process(self, context: ModuleContext) -> ModuleResult:
        # 在同步调用链中返回当前降级强度
        result = ModuleResult()
        result.metrics['current_influence'] = self.influence_level
        return result
