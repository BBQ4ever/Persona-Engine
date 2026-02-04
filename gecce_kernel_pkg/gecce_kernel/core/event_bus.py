"""
GECCE Event Bus - 事件总线

EventBus是GECCE的中枢神经系统，负责：
1. 事件发布/订阅
2. 事件日志记录（用于Replay）
3. 事件优先级处理
4. 异步事件处理

哲学约束：
- 所有事件必须可回放（Replay Engine基础）
- 所有事件必须可追溯
- EventLog是Source of Truth
- 低耦合（模块间只通过EventBus通信）
"""

from loguru import logger
import threading
import queue
from typing import Dict, List, Callable, Optional, Any
from collections import defaultdict
from datetime import datetime
import asyncio
from pathlib import Path
try:
    import msgpack
except ImportError:
    msgpack = None

from .types import Event, EventType


class EventLog:
    """
    事件日志 - Source of Truth
    
    基于用户决策：
    - Tick级粒度
    - 100%可重演
    - 完整记录所有事件
    
    EventLog + StateSnapshot = 完整系统状态
    """
    
    def __init__(self, enable_persistence: bool = True):
        self._log: List[Event] = []
        self._enable_persistence = enable_persistence
        self._lock = threading.Lock()
    
    def append(self, event: Event) -> None:
        """追加事件到日志"""
        with self._lock:
            self._log.append(event)
    
    def get_range(
        self, 
        start_time: datetime, 
        end_time: Optional[datetime] = None
    ) -> List[Event]:
        """
        获取时间范围内的事件
        
        用于Replay Engine
        """
        with self._lock:
            if end_time is None:
                end_time = datetime.now()
            
            return [
                e for e in self._log
                if start_time <= e.timestamp <= end_time
            ]
    
    def get_by_type(self, event_type: EventType) -> List[Event]:
        """获取指定类型的所有事件"""
        with self._lock:
            return [e for e in self._log if e.event_type == event_type]
    
    def get_all(self) -> List[Event]:
        """获取所有事件"""
        with self._lock:
            return self._log.copy()
    
    def save_to_file(self, filepath: str) -> None:
        """
        保存到文件（msgpack格式）
        
        msgpack特性：
        - 比pickle快
        - 比json小
        - 跨语言兼容
        """
        from datetime import datetime
        
        with self._lock:
            data = [e.model_dump(mode='python') for e in self._log]
            
            # 转换datetime为字符串
            for event_data in data:
                if 'timestamp' in event_data and isinstance(event_data['timestamp'], datetime):
                    event_data['timestamp'] = event_data['timestamp'].isoformat()
            
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                msgpack.pack(data, f, use_bin_type=True)
            
            logger.info(f"EventLog saved: {len(self._log)} events -> {filepath}")
    
    def load_from_file(self, filepath: str) -> None:
        """从文件加载"""
        from datetime import datetime
        
        with open(filepath, 'rb') as f:
            data = msgpack.unpack(f, raw=False, strict_map_key=False)
            
            # 转换时间戳字符串回datetime
            for event_data in data:
                if 'timestamp' in event_data and isinstance(event_data['timestamp'], str):
                    event_data['timestamp'] = datetime.fromisoformat(event_data['timestamp'])
            
            self._log = [Event(**e) for e in data]
        
        logger.info(f"EventLog loaded: {len(self._log)} events from {filepath}")
    
    def clear(self) -> None:
        """清空日志（谨慎使用）"""
        with self._lock:
            self._log.clear()
        logger.warning("EventLog cleared")
    
    def __len__(self) -> int:
        return len(self._log)


class EventBus:
    """
    事件总线 - GECCE的中枢神经系统
    
    核心功能：
    1. 发布/订阅模式
    2. 事件日志记录（用于Replay）
    3. 异步事件处理
    4. 事件过滤和路由
    
    哲学约束：
    - 低耦合（模块间只通过EventBus通信）
    - 可记录（所有事件进入EventLog）
    - 可重演（基于EventLog）
    """
    
    def __init__(self, enable_logging: bool = True):
        # 订阅者字典：event_type -> List[callback]
        self._subscribers: Dict[EventType, List[Callable]] = defaultdict(list)
        
        # 事件队列（异步处理）
        self._event_queue: queue.Queue = queue.Queue()
        
        # 处理线程
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
        # 事件日志（用于Replay）
        self._enable_logging = enable_logging
        self._event_log = EventLog() if enable_logging else None
        
        # 统计信息
        self._stats = {
            "published": 0,
            "processed": 0,
            "errors": 0
        }
        
        self._stats_lock = threading.Lock()
    
    def start(self) -> None:
        """启动事件处理线程"""
        if self._running:
            logger.warning("EventBus already running")
            return
        
        self._running = True
        self._thread = threading.Thread(
            target=self._process_events, 
            daemon=True,
            name="EventBus-Processor"
        )
        self._thread.start()
        logger.info("✅ EventBus started")
    
    def stop(self) -> None:
        """停止事件处理线程"""
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        
        logger.info("✅ EventBus stopped")
    
    def subscribe(
        self, 
        event_type: EventType, 
        callback: Callable[[Event], None]
    ) -> None:
        """
        订阅事件类型
        
        Args:
            event_type: 事件类型
            callback: 回调函数，接收Event参数
        """
        self._subscribers[event_type].append(callback)
        logger.debug(
            f"Subscribed to {event_type.value}: "
            f"{callback.__name__ if hasattr(callback, '__name__') else callback}"
        )
    
    def unsubscribe(
        self,
        event_type: EventType,
        callback: Callable[[Event], None]
    ) -> None:
        """取消订阅"""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from {event_type.value}")
            except ValueError:
                pass
    
    def publish(self, event: Event) -> None:
        """
        发布事件
        
        Args:
            event: 事件对象
        
        事件处理流程：
        1. 记录到EventLog（用于Replay）
        2. 放入队列异步处理
        3. 更新统计信息
        """
        # 1. 记录到EventLog（用于Replay）
        if self._enable_logging and self._event_log:
            self._event_log.append(event)
        
        # 2. 放入队列异步处理
        self._event_queue.put(event)
        
        # 3. 更新统计
        with self._stats_lock:
            self._stats["published"] += 1
        
        logger.debug(
            f"Event published: {event.event_type.value} "
            f"from {event.source} (id={event.event_id})"
        )
    
    def _process_events(self) -> None:
        """
        事件处理循环
        
        在独立线程中运行，从队列中取出事件并分发到订阅者
        """
        logger.info("Event processing loop started")
        
        while self._running:
            try:
                # 阻塞等待事件，超时1秒
                event = self._event_queue.get(timeout=1.0)
                
                # 分发到订阅者
                self._dispatch_event(event)
                
                # 更新统计
                with self._stats_lock:
                    self._stats["processed"] += 1
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in event processing loop: {e}", exc_info=True)
                with self._stats_lock:
                    self._stats["errors"] += 1
        
        logger.info("Event processing loop stopped")
    
    def _dispatch_event(self, event: Event) -> None:
        """
        分发事件到订阅者
        
        Args:
            event: 事件对象
        """
        subscribers = self._subscribers.get(event.event_type, [])
        
        if not subscribers:
            logger.debug(f"No subscribers for event type: {event.event_type.value}")
            return
        
        for callback in subscribers:
            try:
                callback(event)
            except Exception as e:
                callback_name = getattr(callback, '__name__', str(callback))
                logger.error(
                    f"Error in event handler {callback_name} "
                    f"for event {event.event_type.value}: {e}",
                    exc_info=True
                )
                with self._stats_lock:
                    self._stats["errors"] += 1
    
    def get_event_log(self) -> Optional[EventLog]:
        """获取事件日志（用于Replay Engine）"""
        return self._event_log
    
    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        with self._stats_lock:
            return {
                **self._stats,
                "event_log_size": len(self._event_log) if self._event_log else 0,
                "queue_size": self._event_queue.qsize(),
                "subscriber_types": len(self._subscribers)
            }
    
    def save_event_log(self, filepath: str) -> None:
        """保存事件日志到文件"""
        if self._event_log:
            self._event_log.save_to_file(filepath)
        else:
            logger.warning("EventLog not enabled, cannot save")
    
    def load_event_log(self, filepath: str) -> None:
        """从文件加载事件日志"""
        if self._event_log:
            self._event_log.load_from_file(filepath)
        else:
            logger.warning("EventLog not enabled, cannot load")
