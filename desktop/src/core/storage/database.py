"""
本地存储模块
使用SQLite存储聊天记录、设备信息、群组信息等
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Optional, Tuple
from pathlib import Path


class Database:
    """数据库管理类"""
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库
        
        Args:
            db_path: 数据库文件路径
        """
        if db_path is None:
            # 默认保存在用户目录
            app_dir = Path.home() / '.tinyim'
            app_dir.mkdir(exist_ok=True)
            db_path = app_dir / 'tinyim.db'
        
        self.db_path = str(db_path)
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # 允许通过列名访问
        
        cursor = self.conn.cursor()
        
        # 创建设备表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                ip_address TEXT,
                avatar_path TEXT,
                remark TEXT,
                last_seen TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建消息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                msg_id TEXT PRIMARY KEY,
                sender_id TEXT NOT NULL,
                receiver_id TEXT NOT NULL,
                msg_type TEXT NOT NULL,
                content TEXT,
                timestamp TEXT NOT NULL,
                is_group INTEGER DEFAULT 0,
                is_read INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建群组表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                announcement TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建群成员表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                group_id TEXT NOT NULL,
                device_id TEXT NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (group_id, device_id)
            )
        ''')
        
        # 创建设置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建文件传输记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_transfers (
                transfer_id TEXT PRIMARY KEY,
                msg_id TEXT,
                filename TEXT,
                filesize INTEGER,
                file_path TEXT,
                status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    # ==================== 设备相关操作 ====================
    
    def save_device(self, device_info: dict):
        """
        保存或更新设备信息
        
        Args:
            device_info: 设备信息字典
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO devices 
            (device_id, nickname, ip_address, avatar_path, last_seen)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            device_info['device_id'],
            device_info['nickname'],
            device_info.get('ip_address'),
            device_info.get('avatar_path'),
            datetime.now().isoformat()
        ))
        self.conn.commit()
    
    def get_device(self, device_id: str) -> Optional[dict]:
        """
        获取设备信息
        
        Args:
            device_id: 设备ID
            
        Returns:
            Optional[dict]: 设备信息
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM devices WHERE device_id = ?', (device_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_devices(self) -> List[dict]:
        """
        获取所有设备
        
        Returns:
            List[dict]: 设备列表
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM devices ORDER BY last_seen DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_device_remark(self, device_id: str, remark: str):
        """
        更新设备备注
        
        Args:
            device_id: 设备ID
            remark: 备注名
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE devices SET remark = ? WHERE device_id = ?',
            (remark, device_id)
        )
        self.conn.commit()
    
    # ==================== 消息相关操作 ====================
    
    def save_message(self, message: dict):
        """
        保存消息
        
        Args:
            message: 消息字典
        """
        cursor = self.conn.cursor()
        
        # 如果content是字典或列表，转为JSON字符串
        content = message['content']
        if isinstance(content, (dict, list)):
            content = json.dumps(content)
        
        cursor.execute('''
            INSERT OR REPLACE INTO messages 
            (msg_id, sender_id, receiver_id, msg_type, content, timestamp, is_group, is_read)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            message['msg_id'],
            message['sender_id'],
            message['receiver_id'],
            message['msg_type'],
            content,
            message['timestamp'],
            1 if message.get('is_group') else 0,
            1 if message.get('is_read') else 0
        ))
        self.conn.commit()
    
    def get_messages(self, peer_id: str, is_group: bool = False, 
                     limit: int = 50, offset: int = 0) -> List[dict]:
        """
        获取与某个对等方的消息历史
        
        Args:
            peer_id: 对方ID（设备ID或群ID）
            is_group: 是否为群聊
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            List[dict]: 消息列表
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM messages 
            WHERE receiver_id = ? AND is_group = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (peer_id, 1 if is_group else 0, limit, offset))
        
        messages = []
        for row in cursor.fetchall():
            msg = dict(row)
            # 尝试解析JSON content
            try:
                msg['content'] = json.loads(msg['content'])
            except (json.JSONDecodeError, TypeError):
                pass  # 保持原样
            messages.append(msg)
        
        return messages
    
    def mark_message_read(self, msg_id: str):
        """
        标记消息为已读
        
        Args:
            msg_id: 消息ID
        """
        cursor = self.conn.cursor()
        cursor.execute('UPDATE messages SET is_read = 1 WHERE msg_id = ?', (msg_id,))
        self.conn.commit()
    
    def delete_message(self, msg_id: str):
        """
        删除消息
        
        Args:
            msg_id: 消息ID
        """
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM messages WHERE msg_id = ?', (msg_id,))
        self.conn.commit()
    
    def delete_chat_history(self, peer_id: str, is_group: bool = False):
        """
        删除与某个对等方的所有聊天记录
        
        Args:
            peer_id: 对方ID
            is_group: 是否为群聊
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'DELETE FROM messages WHERE receiver_id = ? AND is_group = ?',
            (peer_id, 1 if is_group else 0)
        )
        self.conn.commit()
    
    # ==================== 群组相关操作 ====================
    
    def create_group(self, group_info: dict):
        """
        创建群组
        
        Args:
            group_info: 群组信息
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO groups (group_id, group_name, creator_id, announcement)
            VALUES (?, ?, ?, ?)
        ''', (
            group_info['group_id'],
            group_info['group_name'],
            group_info['creator_id'],
            group_info.get('announcement', '')
        ))
        
        # 添加群成员
        for member_id in group_info.get('members', []):
            cursor.execute('''
                INSERT OR IGNORE INTO group_members (group_id, device_id)
                VALUES (?, ?)
            ''', (group_info['group_id'], member_id))
        
        self.conn.commit()
    
    def get_group(self, group_id: str) -> Optional[dict]:
        """
        获取群组信息
        
        Args:
            group_id: 群组ID
            
        Returns:
            Optional[dict]: 群组信息
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        group = dict(row)
        
        # 获取群成员
        cursor.execute(
            'SELECT device_id FROM group_members WHERE group_id = ?',
            (group_id,)
        )
        group['members'] = [row[0] for row in cursor.fetchall()]
        
        return group
    
    def get_all_groups(self) -> List[dict]:
        """
        获取所有群组
        
        Returns:
            List[dict]: 群组列表
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM groups ORDER BY created_at DESC')
        
        groups = []
        for row in cursor.fetchall():
            group = dict(row)
            # 获取群成员
            cursor.execute(
                'SELECT device_id FROM group_members WHERE group_id = ?',
                (group['group_id'],)
            )
            group['members'] = [r[0] for r in cursor.fetchall()]
            groups.append(group)
        
        return groups
    
    # ==================== 设置相关操作 ====================
    
    def save_setting(self, key: str, value: str):
        """
        保存设置
        
        Args:
            key: 设置键
            value: 设置值
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        self.conn.commit()
    
    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """
        获取设置
        
        Args:
            key: 设置键
            default: 默认值
            
        Returns:
            Optional[str]: 设置值
        """
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row[0] if row else default
