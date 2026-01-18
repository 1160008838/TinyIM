"""
应用程序控制器
整合各个模块，提供统一的API
"""
from typing import Callable, Optional
from .core import (
    DeviceManager, DeviceDiscovery, DeviceInfo,
    TCPServer, TCPClient, MessageQueue,
    Message, MessageType,
    Database
)


class TinyIMApp:
    """TinyIM应用程序主控制器"""
    
    def __init__(self):
        """初始化应用程序"""
        # 初始化数据库
        self.db = Database()
        
        # 初始化设备管理器
        self.device_manager = DeviceManager()
        
        # 从数据库加载本地设备信息
        self._load_local_device()
        
        # 初始化网络模块
        self.tcp_server = TCPServer(callback=self._handle_incoming_message)
        self.message_queue = MessageQueue()
        
        # 初始化设备发现
        self.discovery = DeviceDiscovery(
            self.device_manager.local_device,
            callback=self._handle_discovery_event
        )
        
        # 回调函数
        self.message_callback = None
        self.device_callback = None
        
    def start(self):
        """启动应用程序"""
        print("Starting TinyIM...")
        
        # 启动TCP服务器
        self.tcp_server.start()
        
        # 启动消息队列
        self.message_queue.start()
        
        # 启动设备发现
        self.discovery.start()
        
        print(f"TinyIM started! Device ID: {self.device_manager.local_device.device_id}")
        print(f"Local IP: {self.device_manager.local_device.ip_address}")
    
    def stop(self):
        """停止应用程序"""
        print("Stopping TinyIM...")
        
        # 停止设备发现
        self.discovery.stop()
        
        # 停止消息队列
        self.message_queue.stop()
        
        # 停止TCP服务器
        self.tcp_server.stop()
        
        # 关闭数据库
        self.db.close()
        
        print("TinyIM stopped.")
    
    def set_message_callback(self, callback: Callable):
        """
        设置消息回调函数
        
        Args:
            callback: 回调函数，参数为Message对象
        """
        self.message_callback = callback
    
    def set_device_callback(self, callback: Callable):
        """
        设置设备回调函数
        
        Args:
            callback: 回调函数，参数为事件类型和设备信息
        """
        self.device_callback = callback
    
    def _load_local_device(self):
        """从数据库加载本地设备信息"""
        # 获取保存的昵称和头像
        nickname = self.db.get_setting('local_nickname')
        avatar_path = self.db.get_setting('local_avatar')
        
        if nickname:
            self.device_manager.local_device.nickname = nickname
        if avatar_path:
            self.device_manager.local_device.avatar_path = avatar_path
    
    def _handle_incoming_message(self, message_dict: dict):
        """
        处理接收到的消息
        
        Args:
            message_dict: 消息字典
        """
        try:
            # 创建Message对象
            message = Message.from_dict(message_dict)
            
            # 保存到数据库
            self.db.save_message(message.to_dict())
            
            # 调用回调函数
            if self.message_callback:
                self.message_callback(message)
                
        except Exception as e:
            print(f"Handle incoming message error: {e}")
    
    def _handle_discovery_event(self, event_type: str, device_data: dict):
        """
        处理设备发现事件
        
        Args:
            event_type: 事件类型 (device_found/device_left)
            device_data: 设备数据
        """
        try:
            device = DeviceInfo.from_dict(device_data)
            
            if event_type == 'device_found':
                # 添加或更新设备
                self.device_manager.add_device(device)
                self.db.save_device(device_data)
                print(f"Device found: {device.nickname} ({device.ip_address})")
                
            elif event_type == 'device_left':
                # 标记设备离线
                self.device_manager.update_device_status(device.device_id, False)
                print(f"Device left: {device.nickname}")
            
            # 调用回调函数
            if self.device_callback:
                self.device_callback(event_type, device)
                
        except Exception as e:
            print(f"Handle discovery event error: {e}")
    
    # ==================== 消息发送相关 ====================
    
    def send_message(self, receiver_id: str, msg_type: MessageType, 
                     content: any, is_group: bool = False):
        """
        发送消息
        
        Args:
            receiver_id: 接收者ID
            msg_type: 消息类型
            content: 消息内容
            is_group: 是否为群消息
        """
        # 创建消息对象
        message = Message(
            sender_id=self.device_manager.local_device.device_id,
            receiver_id=receiver_id,
            msg_type=msg_type,
            content=content,
            is_group=is_group
        )
        
        # 保存到本地数据库
        self.db.save_message(message.to_dict())
        
        # 发送到对方
        if is_group:
            # 群消息：发送给群里所有成员
            group = self.db.get_group(receiver_id)
            if group:
                for member_id in group['members']:
                    if member_id != self.device_manager.local_device.device_id:
                        device = self.device_manager.get_device(member_id)
                        if device and device.is_online:
                            self.message_queue.enqueue(
                                device.ip_address,
                                message.to_dict()
                            )
        else:
            # 单聊消息
            device = self.device_manager.get_device(receiver_id)
            if device and device.is_online:
                self.message_queue.enqueue(
                    device.ip_address,
                    message.to_dict()
                )
    
    def send_text(self, receiver_id: str, text: str, is_group: bool = False):
        """发送文本消息"""
        self.send_message(receiver_id, MessageType.TEXT, text, is_group)
    
    def send_image(self, receiver_id: str, image_path: str, is_group: bool = False):
        """发送图片消息"""
        self.send_message(receiver_id, MessageType.IMAGE, 
                         {'path': image_path}, is_group)
    
    def send_file(self, receiver_id: str, file_path: str, is_group: bool = False):
        """发送文件消息"""
        import os
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        
        self.send_message(receiver_id, MessageType.FILE, {
            'filename': filename,
            'filesize': filesize,
            'path': file_path
        }, is_group)
    
    # ==================== 设备相关 ====================
    
    def update_profile(self, nickname: str = None, avatar_path: str = None):
        """
        更新个人资料
        
        Args:
            nickname: 新昵称
            avatar_path: 新头像路径
        """
        if nickname:
            self.device_manager.local_device.nickname = nickname
            self.db.save_setting('local_nickname', nickname)
        
        if avatar_path:
            self.device_manager.local_device.avatar_path = avatar_path
            self.db.save_setting('local_avatar', avatar_path)
        
        # 重新公告设备信息
        self.discovery.send_announce()
    
    def get_online_devices(self) -> list:
        """获取在线设备列表"""
        return self.device_manager.get_online_devices()
    
    def get_device_info(self, device_id: str) -> Optional[DeviceInfo]:
        """获取设备信息"""
        return self.device_manager.get_device(device_id)
    
    # ==================== 消息历史相关 ====================
    
    def get_chat_history(self, peer_id: str, is_group: bool = False, 
                         limit: int = 50) -> list:
        """
        获取聊天历史
        
        Args:
            peer_id: 对方ID
            is_group: 是否为群聊
            limit: 数量限制
            
        Returns:
            list: 消息列表
        """
        return self.db.get_messages(peer_id, is_group, limit)
    
    def delete_chat_history(self, peer_id: str, is_group: bool = False):
        """删除聊天历史"""
        self.db.delete_chat_history(peer_id, is_group)
    
    # ==================== 群组相关 ====================
    
    def create_group(self, group_name: str, member_ids: list) -> str:
        """
        创建群组
        
        Args:
            group_name: 群名称
            member_ids: 成员ID列表
            
        Returns:
            str: 群组ID
        """
        import uuid
        group_id = str(uuid.uuid4())
        
        # 添加创建者
        if self.device_manager.local_device.device_id not in member_ids:
            member_ids.append(self.device_manager.local_device.device_id)
        
        group_info = {
            'group_id': group_id,
            'group_name': group_name,
            'creator_id': self.device_manager.local_device.device_id,
            'members': member_ids
        }
        
        self.db.create_group(group_info)
        return group_id
    
    def get_groups(self) -> list:
        """获取所有群组"""
        return self.db.get_all_groups()
