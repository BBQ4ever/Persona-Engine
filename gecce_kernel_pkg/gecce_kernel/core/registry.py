"""
GECCE Module Registry - 模块注册表

ModuleRegistry负责：
1. 模块注册和管理
2. 模块生命周期控制
3. 模块状态查询
4. 降级模式下的模块控制

哲学约束：
- 模块间不得直接耦合
- 所有通信通过EventBus
- 支持动态启用/禁用
"""

from loguru import logger
from typing import Dict, Any, Callable, Optional, List

from .types import ModuleStatus, ModuleType


class ModuleInfo:
    """
    模块信息
    
    记录模块的元数据和状态
    """
    
    def __init__(
        self,
        name: str,
        module_type: ModuleType,
        instance: Any,
        priority: int = 0,
        description: str = ""
    ):
        self.name = name
        self.module_type = module_type
        self.instance = instance
        self.priority = priority
        self.description = description
        self.status = ModuleStatus.REGISTERED
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "type": self.module_type.value,
            "status": self.status.value,
            "priority": self.priority,
            "description": self.description
        }


class ModuleRegistry:
    """
    模块注册表
    
    核心功能：
    1. 注册模块
    2. 启动/停止模块
    3. 启用/禁用模块
    4. 查询模块状态
    
    哲学约束：
    - 模块间通信只能通过EventBus
    - 支持降级模式的模块控制
    """
    
    def __init__(self):
        self._modules: Dict[str, ModuleInfo] = {}
        logger.info("ModuleRegistry initialized")
    
    def register(
        self,
        name: str,
        module_type: ModuleType,
        instance: Any,
        priority: int = 0,
        description: str = ""
    ) -> None:
        """
        注册模块
        
        Args:
            name: 模块名称（唯一标识）
            module_type: 模块类型
            instance: 模块实例
            priority: 优先级（数字越大优先级越高）
            description: 模块描述
        """
        if name in self._modules:
            logger.warning(f"Module already registered: {name}")
            return
        
        module_info = ModuleInfo(
            name, 
            module_type, 
            instance, 
            priority, 
            description
        )
        self._modules[name] = module_info
        
        logger.info(
            f"Module registered: {name} "
            f"(type={module_type.value}, priority={priority})"
        )
    
    def unregister(self, name: str) -> bool:
        """
        注销模块
        
        Args:
            name: 模块名称
            
        Returns:
            是否成功注销
        """
        if name not in self._modules:
            logger.warning(f"Module not found: {name}")
            return False
        
        del self._modules[name]
        logger.info(f"Module unregistered: {name}")
        return True
    
    def get(self, name: str) -> Optional[Any]:
        """
        获取模块实例
        
        Args:
            name: 模块名称
            
        Returns:
            模块实例，如果不存在返回None
        """
        module_info = self._modules.get(name)
        return module_info.instance if module_info else None
    
    def get_info(self, name: str) -> Optional[ModuleInfo]:
        """获取模块信息"""
        return self._modules.get(name)
    
    def disable_module(self, name: str) -> bool:
        """
        禁用模块
        
        Args:
            name: 模块名称
            
        Returns:
            是否成功禁用
        """
        module_info = self._modules.get(name)
        if not module_info:
            logger.warning(f"Module not found: {name}")
            return False
        
        module_info.status = ModuleStatus.DISABLED
        logger.info(f"Module disabled: {name}")
        return True
    
    def enable_module(self, name: str) -> bool:
        """
        启用模块
        
        Args:
            name: 模块名称
            
        Returns:
            是否成功启用
        """
        module_info = self._modules.get(name)
        if not module_info:
            logger.warning(f"Module not found: {name}")
            return False
        
        module_info.status = ModuleStatus.RUNNING
        logger.info(f"Module enabled: {name}")
        return True
    
    def disable_all_except(self, keep_modules: List[str]) -> int:
        """
        禁用除指定模块外的所有模块
        
        Args:
            keep_modules: 保留的模块名称列表
            
        Returns:
            禁用的模块数量
        """
        disabled_count = 0
        
        for name, module_info in self._modules.items():
            if name not in keep_modules:
                module_info.status = ModuleStatus.DISABLED
                disabled_count += 1
        
        logger.info(
            f"All modules disabled except: {keep_modules} "
            f"(disabled {disabled_count} modules)"
        )
        return disabled_count
    
    def set_all_readonly(self) -> int:
        """
        设置所有模块为只读模式
        
        Returns:
            设置的模块数量
        """
        count = 0
        
        for module_info in self._modules.values():
            module_info.status = ModuleStatus.PAUSED
            count += 1
        
        logger.info(f"All modules set to read-only mode ({count} modules)")
        return count
    
    def stop_all(self) -> int:
        """
        停止所有模块
        
        Returns:
            停止的模块数量
        """
        count = 0
        errors = 0
        
        for name, module_info in self._modules.items():
            try:
                # 如果模块有stop方法，调用它
                if hasattr(module_info.instance, 'stop'):
                    module_info.instance.stop()
                
                module_info.status = ModuleStatus.PAUSED
                count += 1
                
            except Exception as e:
                logger.error(f"Error stopping module {name}: {e}")
                module_info.status = ModuleStatus.ERROR
                errors += 1
        
        logger.info(
            f"Stopped {count} modules "
            f"({errors} errors)" if errors > 0 else f"Stopped {count} modules"
        )
        return count
    
    def list_modules(self) -> List[Dict[str, Any]]:
        """
        列出所有模块
        
        Returns:
            模块信息列表
        """
        return [info.to_dict() for info in self._modules.values()]
    
    def get_modules_by_type(self, module_type: ModuleType) -> List[ModuleInfo]:
        """
        根据类型获取模块
        
        Args:
            module_type: 模块类型
            
        Returns:
            模块信息列表
        """
        return [
            info for info in self._modules.values()
            if info.module_type == module_type
        ]
    
    def get_modules_by_status(self, status: ModuleStatus) -> List[ModuleInfo]:
        """
        根据状态获取模块
        
        Args:
            status: 模块状态
            
        Returns:
            模块信息列表
        """
        return [
            info for info in self._modules.values()
            if info.status == status
        ]
    
    def get_enabled_modules(self, sort_by_priority: bool = False) -> List[ModuleInfo]:
        """
        获取所有启用的模块
        
        Args:
            sort_by_priority: 是否按优先级排序
            
        Returns:
            启用的模块信息列表
        """
        enabled = [
            info for info in self._modules.values()
            if info.status == ModuleStatus.RUNNING
        ]
        
        if sort_by_priority:
            enabled.sort(key=lambda x: x.priority, reverse=True)
        
        return enabled
    
    def get_stats(self) -> Dict[str, int]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        stats = {
            "total": len(self._modules),
            "running": 0,
            "disabled": 0,
            "paused": 0,
            "error": 0
        }
        
        for module_info in self._modules.values():
            if module_info.status == ModuleStatus.RUNNING:
                stats["running"] += 1
            elif module_info.status == ModuleStatus.DISABLED:
                stats["disabled"] += 1
            elif module_info.status == ModuleStatus.PAUSED:
                stats["paused"] += 1
            elif module_info.status == ModuleStatus.ERROR:
                stats["error"] += 1
        
        return stats
    
    def __len__(self) -> int:
        return len(self._modules)
    
    def __contains__(self, name: str) -> bool:
        return name in self._modules


# 全局单例
_global_registry: Optional[ModuleRegistry] = None


def get_global_registry() -> ModuleRegistry:
    """
    获取全局ModuleRegistry单例
    
    Returns:
        全局ModuleRegistry实例
    """
    global _global_registry
    
    if _global_registry is None:
        _global_registry = ModuleRegistry()
        logger.info("Global ModuleRegistry created")
    
    return _global_registry


def reset_global_registry() -> None:
    """重置全局Registry（主要用于测试）"""
    global _global_registry
    _global_registry = None
    logger.info("Global ModuleRegistry reset")


def register_module(
    name: str,
    module_type: ModuleType = ModuleType.FEATURE_MODULE,
    priority: int = 0,
    description: str = "",
    tags: Optional[List[str]] = None,
    enabled: bool = True
):
    """
    模块注册装饰器
    
    使用方法:
        @register_module(
            name="my_module",
            module_type=ModuleType.FEATURE_MODULE,
            tags=["tag1", "tag2"],
            enabled=True
        )
        class MyModule:
            pass
    
    Args:
        name: 模块名称
        module_type: 模块类型
        priority: 优先级
        description: 描述
        tags: 模块标签列表
        enabled: 是否启用
    
    Returns:
        装饰器函数
    """
    def decorator(cls):
        """装饰器内部函数"""
        # 只有在enabled=True时才注册
        if enabled:
            # 注册到全局Registry
            instance = cls()
            registry = get_global_registry()
            registry.register(
                name=name,
                module_type=module_type,
                instance=instance,
                priority=priority,
                description=description
            )
        return cls
    
    return decorator
