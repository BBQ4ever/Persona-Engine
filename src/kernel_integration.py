import sys
import os
import json
import time

# Ensure gecce_kernel_pkg is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gecce_kernel_pkg")))

from gecce_kernel.core.event_bus import EventBus
from gecce_kernel.core.registry import ModuleRegistry
from gecce_kernel.core.types import Event, EventType
from gecce_kernel.core.modules.base_module import BaseFeatureModule, ModuleContext, ModuleResult

class PersonaKernel:
    """
    Persona Engine 的内核管理器，封装了 GECCE Kernel 的核心功能。
    """
    def __init__(self):
        self.bus = EventBus(enable_logging=True)
        self.registry = ModuleRegistry()
        self._initialize_infrastructure()

    def _initialize_infrastructure(self):
        self.bus.start()
        print("🚀 Persona Substrate (GECCE Kernel) initialized.")

    def take_snapshot(self, label="manual"):
        """
        捕获所有已注册模块的状态。
        """
        snapshot = {
            "label": label,
            "timestamp": time.time(),
            "module_states": {}
        }
        
        # 遍历 Registry 中的所有模块
        for mod_info in self.registry.list_modules():
            instance = self.registry.get(mod_info['name'])
            if hasattr(instance, 'capture_state'):
                snapshot["module_states"][mod_info['name']] = instance.capture_state()
        
        # 发布快照创建事件
        self.publish_event(EventType.SNAPSHOT_CREATED, "KernelManager", snapshot)
        
        # 也可以保存到本地文件
        os.makedirs("snapshots", exist_ok=True)
        filename = f"snapshots/snapshot_{label}_{int(snapshot['timestamp'])}.json"
        with open(filename, "w") as f:
            json.dump(snapshot, f, indent=2)
            
        print(f"📸 Snapshot '{label}' captured and saved to {filename}")
        return snapshot

    def publish_event(self, event_type: EventType, source: str, data: dict):
        event = Event(
            event_type=event_type,
            source=source,
            data=data
        )
        self.bus.publish(event)

    def subscribe(self, event_type: EventType, callback):
        self.bus.subscribe(event_type, callback)

    def stop(self):
        self.bus.stop()

# 定义 Persona 基础模块类
class PersonaBaseModule(BaseFeatureModule):
    """
    所有内核化的人格模块都应继承此类。
    """
    def __init__(self, bus: EventBus, **kwargs):
        super().__init__(**kwargs)
        self.bus = bus

    def capture_state(self) -> dict:
        """
        返回模块的当前内部状态以便进行快照。
        子类应重写此方法。
        """
        return {}

    def notify_event(self, event_type: EventType, data: dict):
        event = Event(
            event_type=event_type,
            source=self.name,
            data=data
        )
        self.bus.publish(event)
