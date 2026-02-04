# GECCE Kernel Package

GECCE (Global Exchange Chart Computing Engine) 的高性能核心架构库。

## 🎯 核心特性

- **🚀 高性能事件总线**: 异步、非阻塞、支持回放 (Replay) 的事件驱动引擎。
- **🔌 模块化插件系统**: 基于装饰器的自动注册机制，支持热插拔和降级模式。
- **📊 统一数据契约**: 标准化的 `ModuleContext` 和 `ModuleResult`，确保模块间无缝协作。
- **🔍 完整链路追踪**: 内置 `TRACE_ID` 和结构化日志，支持复杂系统的调试与审计。

## 📦 目录结构

```
gecce_kernel/
├── core/
│   ├── event_bus.py       # 异步事件总线
│   ├── registry.py        # 模块注册中心
│   ├── types.py           # 核心类型定义
│   ├── logging_config.py  # 统一日志配置
│   ├── tracing.py         # 链路追踪系统
│   └── modules/
│       └── base_module.py # 模块基类
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install loguru pandas pydantic msgpack
```

### 2. 定义业务模块

只需继承 `BaseFeatureModule` 并使用 `@register_module` 装饰器。

```python
from gecce_kernel.core.modules.base_module import BaseFeatureModule, ModuleContext, ModuleResult
from gecce_kernel.core.registry import register_module

@register_module(name="simple_ma", priority=10)
class MovingAverageModule(BaseFeatureModule):
    def process(self, context: ModuleContext) -> ModuleResult:
        # 获取数据
        df = context.data
        
        # 业务逻辑
        ma_value = df['close'].rolling(window=context.window).mean()
        
        # 返回标准结果
        result = ModuleResult()
        result.metrics['ma'] = ma_value.iloc[-1]
        return result
```

### 3. 使用事件总线

```python
from gecce_kernel.core.event_bus import EventBus
from gecce_kernel.core.types import Event, EventType

# 初始化总线
bus = EventBus()
bus.start()

# 订阅事件
def on_price_tick(event: Event):
    print(f"收到价格更新: {event.data}")

bus.subscribe(EventType.PRICE_TICK, on_price_tick)

# 发布事件
bus.publish(Event(
    event_type=EventType.PRICE_TICK,
    source="market_feed",
    data={"symbol": "AAPL", "price": 150.0}
))
```

## 📖 核心概念

### Event-Driven (事件驱动)
系统通过 `EventBus` 进行解耦。模块不直接相互调用，而是发布事件。这使得系统可以轻松扩展，并支持异步处理密集型任务。

### Kernel-Plugin (内核-插件)
核心逻辑（如 TQS 算法、绘图引擎）被封装为独立的 Modules。`ModuleRegistry` 负责管理这些模块的生命周期。

### Source of Truth (单一事实来源)
`EventLog` 记录了所有发生的事件。通过重放这些事件，可以将系统状态恢复到任意历史时刻。这是回测和故障排查的基础。
