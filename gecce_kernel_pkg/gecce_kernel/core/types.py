"""
GECCE Core Types - 核心数据类型定义

基于GECCE_PHILOSOPHY的核心约束：
1. 所有数据必须可序列化（100%可重演）
2. 所有数据必须带时间戳（因果完整性）
3. 所有数据必须可验证（可审计性）

哲学：结构绝对主义
"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import time


class EventType(str, Enum):
    """事件类型枚举"""
    
    # 市场数据事件
    PRICE_TICK = "price_tick"
    KLINE_UPDATE = "kline_update"
    
    # 特征证据事件
    FEATURE_EVIDENCE = "feature_evidence"
    
    # 结构事件
    STRUCTURE_UPDATE = "structure_update"
    STRUCTURE_CONFIRMED = "structure_confirmed"
    ANCHOR_IDENTIFIED = "anchor_identified"
    THRESHOLD_BROKEN = "threshold_broken"
    
    # 解释层事件（只提供偏置，不改写结构）⚠️
    NARRATIVE_BIAS = "narrative_bias"
    PRECURSOR_SIGNAL = "precursor_signal"
    
    # 风险事件
    SUR_WARNING = "sur_warning"
    CIV_DETECTED = "civ_detected"
    
    # 系统事件
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    SYSTEM_PAUSE = "system_pause"
    DEGRADATION_MODE_CHANGE = "degradation_mode_change"
    SNAPSHOT_CREATED = "snapshot_created"
    
    # --- Persona Engine 扩展 ---
    PERSONA_INPUT = "persona_input"           # 用户输入到达人格层
    PERSONA_STATE_CHANGED = "persona_state_changed" # FSM状态转移
    PERSONA_DEGRADED = "persona_degraded"     # 人格降级触发
    PERSONA_PROJECTION = "persona_projection" # L3输出的权重分布
    SCENE_ANALYZED = "scene_analyzed"         # 场景分析完成
    DRIFT_CHECKED = "drift_checked"           # 漂移检测完成
    TRAITS_SAMPLED = "traits_sampled"         # 采样完成
    ARTIFACT_READY = "artifact_ready"         # 最终结果就绪
    MEMORY_REFINED = "memory_refined"         # 记忆剪枝与整理完成


class Event(BaseModel):
    """
    事件 - GECCE的基础通信单元
    
    哲学约束：
    - 所有事件必须可重演（Replay Engine基础）
    - 所有事件必须带时间戳（因果完整性）
    - 所有事件必须可追溯（可审计性）
    - EventLog是Source of Truth
    """
    
    event_id: str = Field(
        default_factory=lambda: f"evt_{int(time.time() * 1000000)}",
        description="事件唯一ID"
    )
    event_type: EventType = Field(description="事件类型")
    source: str = Field(description="事件来源模块")
    data: Dict[str, Any] = Field(description="事件数据")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="事件时间戳"
    )
    
    # 元数据（用于追溯和审计）
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="事件元数据"
    )
    
    model_config = ConfigDict(
        frozen=True,  # Phase 6.4: Event 不可变
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    def __repr__(self) -> str:
        return f"Event({self.event_type}, source={self.source}, id={self.event_id})"


class DegradationMode(str, Enum):
    """
    降级模式 - 基于用户的业务决策
    
    用户选择：结构纯粹性
    - FULL: 所有模块运行
    - REDUCED: 禁用解释层（NOESIS + FPIA）⭐ 用户的选择
    - MINIMAL: 只运行TQS结构引擎
    - SAFE: 只读模式，不允许交易
    
    哲学：当系统不稳定时，回落到结构，绝不让噪音干扰
    """
    FULL = "full"
    REDUCED = "reduced"  # 用户的降级策略
    MINIMAL = "minimal"
    SAFE = "safe"


class SystemStatus(str, Enum):
    """系统状态"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    DEGRADED = "degraded"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


class ModuleType(str, Enum):
    """模块类型"""
    STRUCTURE_ENGINE = "structure_engine"  # TQS核心
    FEATURE_MODULE = "feature_module"      # 特征模块
    INTERPRETATION = "interpretation"      # 解释层（NOESIS/FPIA）
    VALIDATION = "validation"              # 验证模块（SUR/CIV/SCV）
    RENDERING = "rendering"                # 渲染层


class ModuleStatus(str, Enum):
    """模块状态"""
    REGISTERED = "registered"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    DISABLED = "disabled"
    ERROR = "error"
