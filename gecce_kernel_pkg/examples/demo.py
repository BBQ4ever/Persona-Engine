"""
GECCE Kernel Demo
=================

演示如何使用提取出的核心架构组件构建一个简单的数据处理系统。
"""

import sys
import os
import time
import pandas as pd
from datetime import datetime

# 将包路径添加到 sys.path 以便导入
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gecce_kernel.core.event_bus import EventBus
from gecce_kernel.core.registry import register_module, get_global_registry
from gecce_kernel.core.modules.base_module import BaseFeatureModule, ModuleContext, ModuleResult
from gecce_kernel.core.types import Event, EventType, ModuleType
from gecce_kernel.core.logging_config import setup_gecce_logging, logger

# 1. 初始化日志
setup_gecce_logging(console_level="DEBUG")

# 2. 定义业务模块
@register_module(name="volatility_analyzer", module_type=ModuleType.FEATURE_MODULE, priority=100)
class VolatilityAnalyzer(BaseFeatureModule):
    """一个简单的波动率分析模块"""
    
    def process(self, context: ModuleContext) -> ModuleResult:
        logger.info(f"[{self.name}] 开始分析波动率...")
        
        # 模拟业务逻辑
        df = context.data
        if len(df) < 2:
            return ModuleResult(success=False, error_message="数据不足")
            
        current_price = df['close'].iloc[-1]
        prev_price = df['close'].iloc[-2]
        change = (current_price - prev_price) / prev_price
        
        logger.info(f"[{self.name}] 分析完成: 变化率 {change:.2%}")
        
        result = ModuleResult()
        result.metrics['price_change'] = change
        result.metrics['is_volatile'] = abs(change) > 0.02
        
        return result

# 3. 定义事件处理器
class SystemController:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.registry = get_global_registry()
    
    def on_market_data(self, event: Event):
        logger.info(f"收到市场数据: {event.data}")
        
        # 构造上下文
        data = pd.DataFrame([
            {'close': 100.0, 'timestamp': datetime.now()},
            {'close': event.data.get('price', 100.0), 'timestamp': datetime.now()}
        ])
        
        # 调用注册的模块
        module = self.registry.get("volatility_analyzer")
        if module:
            context = ModuleContext(data=data, params={})
            result = module.execute(context)
            
            # 如果发现高波动，发布警报事件
            if result.success and result.metrics.get('is_volatile'):
                self.bus.publish(Event(
                    event_type=EventType.SUR_WARNING, # 借用现有类型
                    source="volatility_analyzer",
                    data={"message": "检测到剧烈波动！", "change": result.metrics['price_change']}
                ))

def main():
    # 4. 启动系统
    logger.info("🚀 启动 GECCE Kernel Demo")
    
    # 初始化总线
    bus = EventBus()
    bus.start()
    
    # 初始化控制器并订阅
    controller = SystemController(bus)
    bus.subscribe(EventType.PRICE_TICK, controller.on_market_data)
    
    # 模拟数据流
    logger.info("📡 模拟发送市场数据...")
    
    # 第一次：小波动
    bus.publish(Event(
        event_type=EventType.PRICE_TICK,
        source="feed",
        data={"symbol": "BTC", "price": 101.0}
    ))
    
    time.sleep(0.5)
    
    # 第二次：大波动
    bus.publish(Event(
        event_type=EventType.PRICE_TICK,
        source="feed",
        data={"symbol": "BTC", "price": 105.0} # 5% 涨幅
    ))
    
    # 等待异步处理
    time.sleep(1)
    
    # 停止系统
    bus.stop()
    logger.info("✅ Demo 运行结束")

if __name__ == "__main__":
    main()
