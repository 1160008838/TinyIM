"""
消息定义模块
定义各种消息类型和数据结构
"""
from enum import Enum
from datetime import datetime
from typing import Optional, Any
import json


class MessageType(Enum):
    """消息类型枚举"""
    TEXT = 'text'                  # 文字消息
    IMAGE = 'image'                # 图片消息
    FILE = 'file'                  # 文件消息
    VOICE = 'voice'                # 语音消息
    VIDEO = 'video'                # 视频消息
    EMOJI = 'emoji'                # 表情消息
    SYSTEM = 'system'              # 系统消息
    READ_RECEIPT = 'read_receipt'  # 已读回执
    RECALL = 'recall'              # 撤回消息


class Message:
    """消息类"""
    
    def __init__(self, 
                 sender_id: str,
                 receiver_id: str,
                 msg_type: MessageType,
                 content: Any,
                 msg_id: str = None,
                 timestamp: datetime = None,
                 is_group: bool = False,
                 is_read: bool = False):
        """
        初始化消息
        
        Args:
            sender_id: 发送者ID
            receiver_id: 接收者ID (单聊为对方ID，群聊为群ID)
            msg_type: 消息类型
            content: 消息内容
            msg_id: 消息ID (为None时自动生成)
            timestamp: 时间戳
            is_group: 是否为群消息
            is_read: 是否已读
        """
        self.msg_id = msg_id or self._generate_msg_id()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.msg_type = msg_type if isinstance(msg_type, MessageType) else MessageType(msg_type)
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.is_group = is_group
        self.is_read = is_read
    
    @staticmethod
    def _generate_msg_id() -> str:
        """生成消息ID"""
        import uuid
        return str(uuid.uuid4())
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'msg_id': self.msg_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'msg_type': self.msg_type.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'is_group': self.is_group,
            'is_read': self.is_read
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """从字典创建消息"""
        return cls(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            msg_type=MessageType(data['msg_type']),
            content=data['content'],
            msg_id=data.get('msg_id'),
            timestamp=datetime.fromisoformat(data['timestamp']) if 'timestamp' in data else None,
            is_group=data.get('is_group', False),
            is_read=data.get('is_read', False)
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """从JSON字符串创建消息"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __repr__(self) -> str:
        return f"Message(id={self.msg_id[:8]}, type={self.msg_type.value}, from={self.sender_id[:8]})"


class FileMessage:
    """文件消息数据结构"""
    
    def __init__(self, filename: str, filesize: int, file_path: str = None):
        self.filename = filename
        self.filesize = filesize
        self.file_path = file_path
        
    def to_dict(self) -> dict:
        return {
            'filename': self.filename,
            'filesize': self.filesize,
            'file_path': self.file_path
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FileMessage':
        return cls(
            filename=data['filename'],
            filesize=data['filesize'],
            file_path=data.get('file_path')
        )


class GroupInfo:
    """群组信息"""
    
    def __init__(self, group_id: str, group_name: str, 
                 creator_id: str, members: list = None):
        self.group_id = group_id
        self.group_name = group_name
        self.creator_id = creator_id
        self.members = members or []  # list of device_id
        self.announcement = ""
        self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'creator_id': self.creator_id,
            'members': self.members,
            'announcement': self.announcement,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GroupInfo':
        group = cls(
            group_id=data['group_id'],
            group_name=data['group_name'],
            creator_id=data['creator_id'],
            members=data.get('members', [])
        )
        group.announcement = data.get('announcement', '')
        if 'created_at' in data:
            group.created_at = datetime.fromisoformat(data['created_at'])
        return group
