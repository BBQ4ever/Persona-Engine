"""
Base Feature Module
===================

所有 Pipeline Feature Module 的基类模板。

**设计原则**:
- 统一接口（Uniform Interface）
- 可组合（Composable）
- 可测试（Testable）
- 数据驱动（Data-Driven）

作者: BBQ4ever
日期: 2025-12-07
版本: V2.7.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd
from dataclasses import dataclass, field
from ..logging_config import logger


@dataclass
class ModuleContext:
    """
    模块执行上下文
    
    传递给每个 Feature Module 的上下文信息。
    
    Attributes:
        data (pd.DataFrame): 输入数据（K线数据）
        window (int): 窗口大小（用于滑动窗口分析）
        params (Dict[str, Any]): 模块特定参数
        shared_state (Dict[str, Any]): 跨模块共享状态
    """
    data: pd.DataFrame
    window: int = 5
    params: Dict[str, Any] = field(default_factory=dict)
    shared_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleResult:
    """
    模块执行结果
    
    每个 Feature Module 返回的标准结果格式。
    
    Attributes:
        markers (list): 标记数据（高低点等）
        drawings (Dict): 绘图数据（矩形、线段、文字）
        metrics (Dict[str, Any]): 指标数据（用于分析）
        metadata (Dict[str, Any]): 元数据（执行信息）
        success (bool): 是否成功
        error_message (Optional[str]): 错误消息
    """
    markers: list = field(default_factory=list)
    drawings: Dict[str, list] = field(default_factory=lambda: {
        'rectangles': [],
        'lines': [],
        'texts': []
    })
    metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error_message: Optional[str] = None


class BaseFeatureModule(ABC):
    """
    Feature Module 基类
    
    所有 TQS 结构模块都应继承此类。
    
    **子类必须实现**:
    - `process(context)` - 核心处理逻辑
    
    **子类可选实现**:
    - `validate(context)` - 输入验证
    - `setup()` - 初始化逻辑
    - `teardown()` - 清理逻辑
    
    Example:
        >>> class SwingPointsModule(BaseFeatureModule):
        ...     def process(self, context: ModuleContext) -> ModuleResult:
        ...         # 实现高低点检测逻辑
        ...         result = ModuleResult()
        ...         result.markers = [...]
        ...         return result
    """
    
    def __init__(self, **kwargs):
        """
        初始化模块
        
        Args:
            **kwargs: 模块特定配置
        """
        self.config = kwargs
        self.name = self.__class__.__name__
        logger.debug(f"🔧 [Module] 初始化: {self.name}")
    
    @abstractmethod
    def process(self, context: ModuleContext) -> ModuleResult:
        """
        核心处理逻辑（子类必须实现）
        
        Args:
            context (ModuleContext): 执行上下文
        
        Returns:
            ModuleResult: 处理结果
        
        Raises:
            NotImplementedError: 如果子类未实现
        """
        raise NotImplementedError(f"{self.name}.process() must be implemented")
    
    def validate(self, context: ModuleContext) -> bool:
        """
        验证输入数据（可选实现）
        
        Args:
            context (ModuleContext): 执行上下文
        
        Returns:
            bool: 是否验证通过
        """
        # 默认验证：检查数据是否为空
        if context.data is None or context.data.empty:
            logger.error(f"❌ [{self.name}] 数据为空")
            return False
        
        # 默认验证：检查必需列
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required_columns if col not in context.data.columns]
        if missing:
            logger.error(f"❌ [{self.name}] 缺少必需列: {missing}")
            return False
        
        return True
    
    def setup(self) -> None:
        """
        初始化逻辑（可选实现）
        
        在首次调用 process() 前执行。
        """
        pass
    
    def teardown(self) -> None:
        """
        清理逻辑（可选实现）
        
        在模块销毁时执行。
        """
        pass
    
    def execute(self, context: ModuleContext) -> ModuleResult:
        """
        执行模块（包含验证、错误处理）
        
        这是对外暴露的标准接口，不建议子类重写。
        
        Args:
            context (ModuleContext): 执行上下文
        
        Returns:
            ModuleResult: 处理结果
        """
        try:
            logger.debug(f"🚀 [{self.name}] 开始执行")
            
            # 1. 验证输入
            if not self.validate(context):
                return ModuleResult(
                    success=False,
                    error_message=f"Input validation failed for {self.name}"
                )
            
            # 2. 执行处理
            result = self.process(context)
            
            # 3. 添加元数据
            result.metadata['module'] = self.name
            result.metadata['data_length'] = len(context.data)
            result.metadata['window'] = context.window
            
            logger.success(f"✅ [{self.name}] 执行成功")
            return result
        
        except Exception as e:
            logger.error(f"❌ [{self.name}] 执行失败: {e}", exc_info=True)
            return ModuleResult(
                success=False,
                error_message=str(e),
                metadata={'module': self.name}
            )
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key (str): 配置键
            default (Any): 默认值
        
        Returns:
            Any: 配置值
        """
        return self.config.get(key, default)
    
    def __repr__(self) -> str:
        return f"<{self.name} config={self.config}>"


# ========================================
# 便捷的模块结果合并函数
# ========================================

def merge_module_results(results: list[ModuleResult]) -> ModuleResult:
    """
    合并多个模块结果
    
    Args:
        results (list[ModuleResult]): 模块结果列表
    
    Returns:
        ModuleResult: 合并后的结果
    """
    merged = ModuleResult()
    
    for result in results:
        if not result.success:
            merged.success = False
            merged.error_message = (merged.error_message or "") + f"; {result.error_message}"
            continue
        
        # 合并 markers
        merged.markers.extend(result.markers)
        
        # 合并 drawings
        for key in ['rectangles', 'lines', 'texts']:
            merged.drawings[key].extend(result.drawings.get(key, []))
        
        # 合并 metrics
        merged.metrics.update(result.metrics)
        
        # 合并 metadata
        merged.metadata.update(result.metadata)
    
    logger.debug(
        f"🔀 [Merge] 合并 {len(results)} 个结果: "
        f"{len(merged.markers)} markers, "
        f"{sum(len(v) for v in merged.drawings.values())} drawings"
    )
    
    return merged
