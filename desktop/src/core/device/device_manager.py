"""
设备管理模块
用于生成唯一设备ID、管理设备信息
"""
import hashlib
import socket
import uuid
import platform
from typing import Optional


class DeviceInfo:
    """设备信息类"""
    
    def __init__(self, device_id: str = None, nickname: str = None, 
                 ip_address: str = None, avatar_path: str = None):
        """
        初始化设备信息
        
        Args:
            device_id: 设备唯一ID
            nickname: 设备昵称
            ip_address: IP地址
            avatar_path: 头像路径
        """
        self.device_id = device_id or self.generate_device_id()
        self.nickname = nickname or self.generate_default_nickname()
        self.ip_address = ip_address or self.get_local_ip()
        self.avatar_path = avatar_path or "default_avatar.png"
        self.is_online = False
        self.last_seen = None
        
    @staticmethod
    def generate_device_id() -> str:
        """
        生成唯一设备ID
        基于MAC地址和机器UUID生成
        
        Returns:
            str: 设备唯一ID
        """
        # 获取MAC地址
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        
        # 获取机器名称
        hostname = socket.gethostname()
        
        # 获取系统信息
        system_info = f"{platform.system()}{platform.machine()}"
        
        # 组合并生成哈希
        unique_string = f"{mac}-{hostname}-{system_info}"
        device_id = hashlib.sha256(unique_string.encode()).hexdigest()[:16]
        
        return device_id.upper()
    
    @staticmethod
    def generate_default_nickname() -> str:
        """
        生成默认昵称
        
        Returns:
            str: 默认昵称
        """
        import random
        random_suffix = random.randint(1000, 9999)
        return f"Device-{random_suffix}"
    
    @staticmethod
    def get_local_ip() -> str:
        """
        获取本机局域网IP地址
        
        Returns:
            str: IP地址
        """
        try:
            # 创建一个UDP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 不需要真正连接，只是为了获取本地IP
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def to_dict(self) -> dict:
        """
        转换为字典
        
        Returns:
            dict: 设备信息字典
        """
        return {
            'device_id': self.device_id,
            'nickname': self.nickname,
            'ip_address': self.ip_address,
            'avatar_path': self.avatar_path,
            'is_online': self.is_online
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DeviceInfo':
        """
        从字典创建设备信息
        
        Args:
            data: 设备信息字典
            
        Returns:
            DeviceInfo: 设备信息对象
        """
        device = cls(
            device_id=data.get('device_id'),
            nickname=data.get('nickname'),
            ip_address=data.get('ip_address'),
            avatar_path=data.get('avatar_path')
        )
        device.is_online = data.get('is_online', False)
        return device
    
    def __repr__(self) -> str:
        return f"DeviceInfo(id={self.device_id}, name={self.nickname}, ip={self.ip_address})"


class DeviceManager:
    """设备管理器"""
    
    def __init__(self):
        """初始化设备管理器"""
        self.local_device = DeviceInfo()
        self.devices = {}  # device_id -> DeviceInfo
        
    def update_local_device(self, nickname: str = None, avatar_path: str = None):
        """
        更新本地设备信息
        
        Args:
            nickname: 新昵称
            avatar_path: 新头像路径
        """
        if nickname:
            self.local_device.nickname = nickname
        if avatar_path:
            self.local_device.avatar_path = avatar_path
    
    def add_device(self, device: DeviceInfo):
        """
        添加设备
        
        Args:
            device: 设备信息
        """
        self.devices[device.device_id] = device
    
    def remove_device(self, device_id: str):
        """
        移除设备
        
        Args:
            device_id: 设备ID
        """
        if device_id in self.devices:
            del self.devices[device_id]
    
    def get_device(self, device_id: str) -> Optional[DeviceInfo]:
        """
        获取设备信息
        
        Args:
            device_id: 设备ID
            
        Returns:
            Optional[DeviceInfo]: 设备信息，不存在则返回None
        """
        return self.devices.get(device_id)
    
    def get_online_devices(self) -> list:
        """
        获取所有在线设备
        
        Returns:
            list: 在线设备列表
        """
        return [device for device in self.devices.values() if device.is_online]
    
    def update_device_status(self, device_id: str, is_online: bool):
        """
        更新设备在线状态
        
        Args:
            device_id: 设备ID
            is_online: 是否在线
        """
        if device_id in self.devices:
            self.devices[device_id].is_online = is_online
