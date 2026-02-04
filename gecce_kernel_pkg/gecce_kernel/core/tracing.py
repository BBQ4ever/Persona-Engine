"""
GECCE 请求链路追踪系统
=====================

基于Context Variable的TRACE_ID管理
支持异步环境和多线程场景
"""

import uuid
import contextvars
from datetime import datetime
from typing import Optional, Dict, Any
from functools import wraps

# ==========================================
# 🎯 Context Variable（线程安全）
# ==========================================

# 当前请求的TRACE_ID
_trace_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    'trace_id', 
    default=None
)

# 当前请求的额外上下文信息
_trace_context_var: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar(
    'trace_context',
    default=None
)


# ==========================================
# 🔑 TRACE_ID 生成器
# ==========================================

def generate_trace_id() -> str:
    """
    生成唯一的TRACE_ID
    
    格式: TR-{timestamp}-{short_uuid}
    示例: TR-20251207-a3f2
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"TR-{timestamp}-{short_uuid}"


# ==========================================
# 🎯 TRACE_ID 管理函数
# ==========================================

def set_trace_id(trace_id: Optional[str] = None) -> str:
    """
    设置当前请求的TRACE_ID
    
    Args:
        trace_id: 指定的TRACE_ID，如果为None则自动生成
        
    Returns:
        实际使用的TRACE_ID
    """
    if trace_id is None:
        trace_id = generate_trace_id()
    
    _trace_id_var.set(trace_id)
    return trace_id


def get_trace_id() -> str:
    """
    获取当前请求的TRACE_ID
    
    Returns:
        当前TRACE_ID，如果未设置则返回"NO_TRACE"
    """
    trace_id = _trace_id_var.get()
    if trace_id is None:
        return "NO_TRACE"
    return trace_id


def clear_trace_id():
    """清除当前TRACE_ID"""
    _trace_id_var.set(None)


# ==========================================
# 🎯 上下文信息管理
# ==========================================

def set_trace_context(key: str, value: Any):
    """
    设置追踪上下文信息
    
    Args:
        key: 上下文键
        value: 上下文值
    """
    context = _trace_context_var.get()
    if context is None:
        context = {}
        _trace_context_var.set(context)
    context[key] = value


def get_trace_context(key: str = None) -> Any:
    """
    获取追踪上下文信息
    
    Args:
        key: 上下文键，如果为None则返回整个上下文字典
        
    Returns:
        上下文值或整个上下文字典
    """
    context = _trace_context_var.get()
    if context is None:
        return {} if key is None else None
    
    if key is None:
        return context
    return context.get(key)


def clear_trace_context():
    """清除所有追踪上下文"""
    _trace_context_var.set(None)


# ==========================================
# 🎯 装饰器：自动追踪
# ==========================================

def with_trace(auto_generate=True):
    """
    装饰器：为函数调用自动设置TRACE_ID
    
    Args:
        auto_generate: 如果当前没有TRACE_ID，是否自动生成
        
    Example:
        @with_trace()
        def my_function():
            trace_id = get_trace_id()
            print(f"Processing with trace: {trace_id}")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查是否已有TRACE_ID
            existing_trace = _trace_id_var.get()
            
            if existing_trace is None and auto_generate:
                # 自动生成新的TRACE_ID
                trace_id = set_trace_id()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # 如果是本函数生成的TRACE_ID，清理它
                if existing_trace is None and auto_generate:
                    clear_trace_id()
                    clear_trace_context()
        
        return wrapper
    return decorator


# ==========================================
# 🎯 上下文管理器：追踪块
# ==========================================

class TraceContext:
    """
    上下文管理器：在代码块中使用独立的TRACE_ID
    
    Example:
        with TraceContext() as trace_id:
            print(f"Processing: {trace_id}")
            # ... 执行业务逻辑 ...
    """
    
    def __init__(self, trace_id: Optional[str] = None):
        """
        Args:
            trace_id: 指定TRACE_ID，如果为None则自动生成
        """
        self.trace_id = trace_id
        self.previous_trace_id = None
        self.previous_context = None
    
    def __enter__(self):
        # 保存之前的状态
        self.previous_trace_id = _trace_id_var.get()
        self.previous_context = _trace_context_var.get()
        
        # 设置新的TRACE_ID
        self.trace_id = set_trace_id(self.trace_id)
        
        return self.trace_id
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 恢复之前的状态
        if self.previous_trace_id is not None:
            _trace_id_var.set(self.previous_trace_id)
        else:
            clear_trace_id()
        
        if self.previous_context is not None:
            _trace_context_var.set(self.previous_context)
        else:
            clear_trace_context()
        
        return False  # 不抑制异常


# ==========================================
# 🎯 导出
# ==========================================

__all__ = [
    'generate_trace_id',
    'set_trace_id',
    'get_trace_id',
    'clear_trace_id',
    'set_trace_context',
    'get_trace_context',
    'clear_trace_context',
    'with_trace',
    'TraceContext',
]
