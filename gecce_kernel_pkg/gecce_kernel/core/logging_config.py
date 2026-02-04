"""
GECCE 统一日志配置模块
=======================

基于Loguru的高性能调试日志系统

特性:
- 彩色控制台输出
- 自动日志文件轮转
- 异常自动捕获
- 函数调用追踪
- 结构化日志支持
- TRACE_ID 请求链路追踪 (V2.9)
"""

from loguru import logger
import sys
from pathlib import Path
from functools import wraps
import time
from typing import Optional

# ==========================================
# 🎯 V2.9 Phase 4: 立即配置默认extra值
# ==========================================
# 确保即使在setup之前的logger调用也有默认值
logger.configure(
    extra={"trace_id": "NO_TRACE", "module": "SYSTEM"}
)


# ==========================================
# 🎨 日志格式配置 (V2.9 Phase 4)
# ==========================================

# 新格式：[TRACE_ID][MODULE] message
# 符合 plan.md Phase 4 要求

# 控制台格式：V3完整格式（带TRACE_ID和MODULE）
CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>[{extra[trace_id]}]</cyan><blue>[{extra[module]}]</blue> | "
    "{name}:{function}:{line} - <level>{message}</level>\n"
)

# 文件格式：纯文本（带TRACE_ID和MODULE）
FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "[{extra[trace_id]}][{extra[module]}] | "
    "{name}:{function}:{line} - {message}\n"
)


# ==========================================
# 🚀 初始化Loguru
# ==========================================

def _get_current_trace_id():
    """获取当前TRACE_ID（用于patcher）"""
    try:
        from .tracing import get_trace_id
        return get_trace_id()
    except Exception:
        return "NO_TRACE"


def _patcher(record):
    """
    自动注入TRACE_ID和MODULE到日志记录
    
    这样所有logger调用都自动带上当前请求的trace_id和模块名
    不需要手动bind
    """
    # ✅ 总是获取当前trace_id（即使record中有，也用最新的）
    # 这样TraceContext中的trace_id能自动传播
    record["extra"]["trace_id"] = _get_current_trace_id()
    
    # ✅ 如果module是默认值SYSTEM，自动从模块名提取
    # 否则保留用户手动bind的module值
    if record["extra"].get("module") == "SYSTEM":
        # 从record["name"]提取模块名
        # 例如: "src.ui.dashboard.callbacks.data_callbacks" -> "DATA_CALLBACKS"
        module_name = record["name"].split(".")[-1]
        record["extra"]["module"] = module_name.upper()
    
    return record


def setup_gecce_logging(
    console_level="INFO",
    file_level="DEBUG",
    log_dir="logs",
    enable_file=True,
    enable_source_separation=False
):
    """
    配置GECCE项目的统一日志系统（V3完整版）
    
    特性：
    - 自动TRACE_ID注入（无需手动bind）
    - MODULE标签自动提取
    - 彩色控制台输出
    - 多文件分类日志
    - 模块分流（可选）
    
    Args:
        console_level: 控制台日志级别 (DEBUG/INFO/WARNING/ERROR)
        file_level: 文件日志级别
        log_dir: 日志文件目录
        enable_file: 是否启用文件日志
        enable_source_separation: 是否按模块名分流日志到独立文件夹
    """
    # 移除默认handler
    logger.remove()
    
    # ==========================================
    # 🎯 配置默认extra值（V2.9 Phase 4）
    # ==========================================
    # 为所有日志记录自动添加默认 trace_id 和 module
    logger.configure(
        extra={"trace_id": "NO_TRACE", "module": "SYSTEM"},
        patcher=_patcher  # ✅ V3关键：自动注入trace_id
    )
    
    # ==========================================
    # 📺 控制台Handler（彩色输出 + V2.9格式）
    # ==========================================
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level=console_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # ==========================================
    # 📝 文件Handler（详细记录）
    # ==========================================
    if enable_file:
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # 主日志文件（自动轮转）
        # ⚠️ 使用函数formatter避免消息中的{}被误解析为格式占位符
        logger.add(
            log_path / "gecce_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,  # 现在是函数，不是字符串
            level=file_level,
            rotation="00:00",  # 每天午夜轮转
            retention="30 days",  # 保留30天
            compression="zip",  # 压缩旧日志
            backtrace=True,
            diagnose=True,
            enqueue=True  # 异步写入
        )
        
        # 错误日志文件（只记录ERROR和CRITICAL）
        logger.add(
            log_path / "gecce_error_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="ERROR",
            rotation="100 MB",
            retention="60 days",
            compression="zip",
            backtrace=True,
            diagnose=True,
            enqueue=True
        )
        
        # UI渲染专用日志（用于调试前端问题）
        logger.add(
            log_path / "gecce_ui_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="DEBUG",
            rotation="50 MB",
            retention="7 days",
            filter=lambda record: "ui" in record["name"].lower() or "render" in record["message"].lower(),
            backtrace=True,
            enqueue=True
        )
        
        # TQS分析专用日志
        logger.add(
            log_path / "gecce_tqs_{time:YYYY-MM-DD}.log",
            format=FILE_FORMAT,
            level="DEBUG",
            rotation="50 MB",
            retention="14 days",
            filter=lambda record: "tqs" in record["name"].lower(),
            backtrace=True,
            enqueue=True
        )
        
        # ==========================================
        # 📁 模块分流日志（可选）
        # ==========================================
        if enable_source_separation:
            # 为常见模块创建独立的日志handler
            # 每个模块都有自己的日志文件夹
            common_modules = [
                # 核心系统模块
                "KERNEL",
                "EVENT_BUS",
                "STATE_HUB",
                "REGISTRY",
                
                # UI层模块
                "DATA_CALLBACKS",
                "UI_CALLBACK",
                "FRONTEND",
                "FRONTEND_PERF",
                "FRONTEND_CONSOLE",
                "ERROR_REPORT",
                "PERF_REPORT",
                
                # 编排与策略模块
                "ORCHESTRATOR",
                "V4_ORCHESTRATOR",
                "STRATEGY_ROUTER",
                "STRATEGY_STANDARD",
                "STRATEGY_TQS",
                
                # 数据流水线模块
                "KLINE_PIPELINE",
                "TA_PIPELINE",
                "HYBRID_KLINE",
                "TICKPATCH_ENGINE",
                
                # TQS引擎模块
                "TQS_INTEGRATOR",
                "OSCILLATION_AXIS",
                "SWING_POINTS_MODULE",
                
                # 数据处理模块
                "STRUCTURE_LOADER",
                "STRUCTURE_TO_VIEWMODEL",
                "CLEANER",
                
                # 其他模块
                "CACHE_MANAGER",
                "VALIDATOR"
            ]
            
            for module_name in common_modules:
                module_dir = log_path / "modules" / module_name
                module_dir.mkdir(parents=True, exist_ok=True)
                
                logger.add(
                    module_dir / f"{module_name}_{{time:YYYY-MM-DD}}.log",
                    format=FILE_FORMAT,
                    level=file_level,
                    rotation="20 MB",
                    retention="14 days",
                    filter=lambda record, mn=module_name: record['extra'].get('module', '') == mn,
                    backtrace=True,
                    enqueue=True
                )
            
            logger.success(f"📁 模块分流已启用 | 已配置 {len(common_modules)} 个模块")
    
    logger.success(f"GECCE logging system initialized | Console: {console_level} | File: {file_level}")
    return logger


# ==========================================
# 🎯 装饰器：自动记录函数调用
# ==========================================

def log_function_call(log_args=True, log_result=False, log_time=True):
    """
    装饰器：自动记录函数调用信息
    
    Args:
        log_args: 是否记录参数
        log_result: 是否记录返回值
        log_time: 是否记录执行时间
        
    Example:
        @log_function_call(log_args=True, log_result=True)
        def my_function(x, y):
            return x + y
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            
            # 记录函数调用
            if log_args:
                args_str = f"args={args}, kwargs={kwargs}"
                logger.debug(f"➡️  [{func_name}] 调用开始 | {args_str}")
            else:
                logger.debug(f"➡️  [{func_name}] 调用开始")
            
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                
                elapsed = time.perf_counter() - start_time
                
                # 记录返回值和执行时间
                if log_result and log_time:
                    logger.debug(f"✅ [{func_name}] 调用成功 | 耗时: {elapsed*1000:.2f}ms | 返回: {result}")
                elif log_time:
                    logger.debug(f"✅ [{func_name}] 调用成功 | 耗时: {elapsed*1000:.2f}ms")
                elif log_result:
                    logger.debug(f"✅ [{func_name}] 调用成功 | 返回: {result}")
                else:
                    logger.debug(f"✅ [{func_name}] 调用成功")
                
                return result
                
            except Exception as e:
                elapsed = time.perf_counter() - start_time
                logger.exception(f"❌ [{func_name}] 调用失败 | 耗时: {elapsed*1000:.2f}ms | 错误: {e}")
                raise
        
        return wrapper
    return decorator


# ==========================================
# 🎯 装饰器：性能监控
# ==========================================

def log_performance(threshold_ms=100):
    """
    装饰器：监控函数性能，超过阈值时发出警告
    
    Args:
        threshold_ms: 警告阈值（毫秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__name__}"
            start_time = time.perf_counter()
            
            result = func(*args, **kwargs)
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            if elapsed_ms > threshold_ms:
                logger.warning(f"⚠️  [{func_name}] 执行缓慢 | 耗时: {elapsed_ms:.2f}ms (阈值: {threshold_ms}ms)")
            else:
                logger.debug(f"⚡ [{func_name}] 执行完成 | 耗时: {elapsed_ms:.2f}ms")
            
            return result
        
        return wrapper
    return decorator


# ==========================================
# 🎯 便捷函数：结构化日志
# ==========================================

def log_api_call(api_name, endpoint, params=None, status=None, elapsed_ms=None):
    """记录API调用"""
    logger.bind(
        api=api_name,
        endpoint=endpoint,
        params=params,
        status=status,
        elapsed_ms=elapsed_ms
    ).info(f"🌐 API调用 | {api_name}.{endpoint}")


def log_data_processing(step, input_size, output_size, elapsed_ms):
    """记录数据处理步骤"""
    logger.bind(
        step=step,
        input_size=input_size,
        output_size=output_size,
        elapsed_ms=elapsed_ms
    ).info(f"📊 数据处理 | {step} | {input_size}→{output_size} | {elapsed_ms:.2f}ms")


def log_ui_render(component, data_size, elapsed_ms):
    """记录UI渲染"""
    logger.bind(
        component=component,
        data_size=data_size,
        elapsed_ms=elapsed_ms
    ).info(f"🎨 UI渲染 | {component} | 数据量: {data_size} | {elapsed_ms:.2f}ms")


def log_tqs_analysis(analysis_type, symbol, result_count, elapsed_ms):
    """记录TQS分析"""
    logger.bind(
        analysis_type=analysis_type,
        symbol=symbol,
        result_count=result_count,
        elapsed_ms=elapsed_ms
    ).info(f"🧠 TQS分析 | {analysis_type} | {symbol} | 结果: {result_count} | {elapsed_ms:.2f}ms")


# ==========================================
# 🎯 V2.9 Phase 4: 统一日志接口（带TRACE_ID和MODULE）
# ==========================================

def log_with_context(
    message: str, 
    module: str,
    level: str = "INFO",
    trace_id: Optional[str] = None,
    **extra_fields
):
    """
    统一的日志接口（V2.9 Phase 4）
    
    格式: [TRACE_ID][MODULE] message
    
    Args:
        message: 日志消息
        module: 模块名称（如 "ORCHESTRATOR", "KLINE_PIPELINE"）
        level: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
        trace_id: 追踪ID，如果为None则从tracing模块获取
        **extra_fields: 额外的结构化字段
        
    Example:
        log_with_context("开始处理K线数据", "KLINE_PIPELINE", level="INFO")
        log_with_context("发现错误", "TA_PIPELINE", level="ERROR", error_code=500)
    """
    # 如果没有提供trace_id，尝试从tracing模块获取
    if trace_id is None:
        try:
            from .tracing import get_trace_id
            trace_id = get_trace_id()
        except Exception:
            trace_id = "NO_TRACE"
    
    # 绑定trace_id和module
    bound_logger = logger.bind(
        trace_id=trace_id,
        module=module,
        **extra_fields
    )
    
    # 根据级别记录日志
    log_method = getattr(bound_logger, level.lower(), bound_logger.info)
    log_method(message)


def get_module_logger(module: str):
    """
    获取带模块名的logger（便捷工厂函数）
    
    Args:
        module: 模块名称
        
    Returns:
        绑定了模块名的logger函数
        
    Example:
        log = get_module_logger("ORCHESTRATOR")
        log("开始编排", level="INFO")
        log("发生错误", level="ERROR")
    """
    def module_log(message: str, level: str = "INFO", **kwargs):
        log_with_context(message, module=module, level=level, **kwargs)
    
    return module_log


# ==========================================
# 🎯 初始化（V2.9 - 禁用自动初始化）
# ==========================================

# V2.9 Phase 4: 禁用自动初始化，必须显式调用 setup_gecce_logging()
# 这确保所有模块使用相同的日志配置

# if not logger._core.handlers:
#     setup_gecce_logging(
#         console_level="DEBUG",
#         file_level="DEBUG",
#         enable_file=True
#     )


# 导出便捷的logger实例
__all__ = [
    'logger',
    'setup_gecce_logging',
    'log_function_call',
    'log_performance',
    'log_api_call',
    'log_data_processing',
    'log_ui_render',
    'log_tqs_analysis',
    # V2.9 Phase 4 新增
    'log_with_context',
    'get_module_logger',
]
