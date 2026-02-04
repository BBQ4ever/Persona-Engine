import sys
import os
import json

# Add path for gecce_kernel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "gecce_kernel_pkg")))

from gecce_kernel.core.types import Event, EventType
from gecce_kernel.core.modules.base_module import ModuleContext, ModuleResult
from kernel_integration import PersonaBaseModule
from .projection import SeededSampler

class KernelExpression(PersonaBaseModule):
    """
    L3 Expression - 内核化版本
    职责：根据基因和当前降级强度，输出最终的人格投影。
    """
    def __init__(self, bus, genome_data, **kwargs):
        super().__init__(bus, **kwargs)
        self.genome = genome_data
        self.sampler = SeededSampler()
        self.current_influence = 1.0
        
        # 订阅输入与降级事件
        self.bus.subscribe(EventType.PERSONA_INPUT, self.on_request)
        self.bus.subscribe(EventType.PERSONA_DEGRADED, self.on_degradation)

    def on_degradation(self, event: Event):
        self.current_influence = event.data.get("target_influence", 1.0)
        print(f"[{self.name}] Influence updated via event: {self.current_influence}")

    def on_request(self, event: Event):
        session_id = event.data.get("session_id", "default_session")
        
        # 执行采样
        projection = {}
        for trait in self.genome['loci']:
            val = self.sampler.sample_trait(
                trait, 
                session_id, 
                influence=self.current_influence
            )
            projection[trait['id']] = val
            
        # 发布投影事件
        self.notify_event(EventType.PERSONA_PROJECTION, {
            "session_id": session_id,
            "projection": projection,
            "influence": self.current_influence
        })

    def capture_state(self) -> dict:
        return {
            "current_influence": self.current_influence,
            "genome_snapshot": self.genome
        }

    def process(self, context: ModuleContext) -> ModuleResult:
        # 同步接口也可以通过 context 传回当前的投影（如果需要）
        return ModuleResult()
