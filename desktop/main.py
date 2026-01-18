#!/usr/bin/env python3
"""
TinyIM 桌面端主程序
命令行界面版本（用于测试和演示）
"""
import sys
import os
import time
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import TinyIMApp
from core.network import MessageType


class TinyIMCLI:
    """TinyIM命令行界面"""
    
    def __init__(self):
        """初始化CLI"""
        self.app = TinyIMApp()
        self.running = False
        
        # 设置回调
        self.app.set_message_callback(self.on_message_received)
        self.app.set_device_callback(self.on_device_event)
        
    def on_message_received(self, message):
        """消息接收回调"""
        device = self.app.get_device_info(message.sender_id)
        sender_name = device.nickname if device else message.sender_id[:8]
        
        print(f"\n[{message.timestamp.strftime('%H:%M:%S')}] {sender_name}: {message.content}")
        print("> ", end='', flush=True)
    
    def on_device_event(self, event_type, device):
        """设备事件回调"""
        if event_type == 'device_found':
            print(f"\n[系统] 发现设备: {device.nickname} ({device.ip_address})")
        elif event_type == 'device_left':
            print(f"\n[系统] 设备离线: {device.nickname}")
        print("> ", end='', flush=True)
    
    def start(self):
        """启动CLI"""
        print("=" * 60)
        print(" " * 20 + "TinyIM 即时通讯")
        print("=" * 60)
        
        # 启动应用
        self.app.start()
        self.running = True
        
        print("\n欢迎使用 TinyIM!")
        print(f"设备ID: {self.app.device_manager.local_device.device_id}")
        print(f"昵称: {self.app.device_manager.local_device.nickname}")
        print(f"IP地址: {self.app.device_manager.local_device.ip_address}")
        print("\n输入 'help' 查看帮助信息\n")
        
        # 主循环
        try:
            while self.running:
                command = input("> ").strip()
                if command:
                    self.handle_command(command)
        except KeyboardInterrupt:
            print("\n正在退出...")
        finally:
            self.stop()
    
    def stop(self):
        """停止CLI"""
        self.running = False
        self.app.stop()
        print("再见!")
    
    def handle_command(self, command: str):
        """处理用户命令"""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'help':
            self.show_help()
        elif cmd == 'list' or cmd == 'ls':
            self.list_devices()
        elif cmd == 'send':
            self.send_message(args)
        elif cmd == 'profile':
            self.update_profile(args)
        elif cmd == 'history':
            self.show_history(args)
        elif cmd == 'clear':
            self.clear_history(args)
        elif cmd == 'group':
            self.handle_group_command(args)
        elif cmd == 'exit' or cmd == 'quit':
            self.running = False
        else:
            print(f"未知命令: {cmd}. 输入 'help' 查看帮助")
    
    def show_help(self):
        """显示帮助信息"""
        print("""
可用命令:
  help              - 显示此帮助信息
  list, ls          - 列出在线设备
  send <id> <msg>   - 发送消息到指定设备
  profile <name>    - 修改昵称
  history <id>      - 查看与指定设备的聊天记录
  clear <id>        - 清除与指定设备的聊天记录
  group create <name> <id1,id2>  - 创建群组
  group list        - 列出所有群组
  exit, quit        - 退出程序

示例:
  list              - 查看在线设备
  send A1B2 你好    - 发送"你好"给设备A1B2
  profile 小明      - 将昵称改为"小明"
        """)
    
    def list_devices(self):
        """列出在线设备"""
        devices = self.app.get_online_devices()
        
        if not devices:
            print("当前没有在线设备")
            return
        
        print(f"\n在线设备 ({len(devices)}个):")
        print("-" * 60)
        for device in devices:
            print(f"  ID: {device.device_id[:8]}...  昵称: {device.nickname:15}  IP: {device.ip_address}")
        print("-" * 60)
    
    def send_message(self, args: str):
        """发送消息"""
        if not args:
            print("用法: send <设备ID前缀> <消息内容>")
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            print("用法: send <设备ID前缀> <消息内容>")
            return
        
        target_prefix, message = parts
        
        # 查找设备
        device = None
        for d in self.app.get_online_devices():
            if d.device_id.startswith(target_prefix.upper()):
                device = d
                break
        
        if not device:
            print(f"未找到ID以 '{target_prefix}' 开头的在线设备")
            return
        
        # 发送消息
        self.app.send_text(device.device_id, message)
        print(f"已发送到 {device.nickname}")
    
    def update_profile(self, nickname: str):
        """更新个人资料"""
        if not nickname:
            print("用法: profile <新昵称>")
            return
        
        self.app.update_profile(nickname=nickname)
        print(f"昵称已更新为: {nickname}")
    
    def show_history(self, device_prefix: str):
        """显示聊天历史"""
        if not device_prefix:
            print("用法: history <设备ID前缀>")
            return
        
        # 查找设备
        device = None
        for d in self.app.device_manager.devices.values():
            if d.device_id.startswith(device_prefix.upper()):
                device = d
                break
        
        if not device:
            print(f"未找到ID以 '{device_prefix}' 开头的设备")
            return
        
        # 获取历史记录
        messages = self.app.get_chat_history(device.device_id, limit=20)
        
        if not messages:
            print(f"与 {device.nickname} 没有聊天记录")
            return
        
        print(f"\n与 {device.nickname} 的聊天记录:")
        print("-" * 60)
        for msg in reversed(messages):  # 按时间正序显示
            sender = "我" if msg['sender_id'] == self.app.device_manager.local_device.device_id else device.nickname
            timestamp = msg['timestamp'][:19]  # 只显示到秒
            print(f"[{timestamp}] {sender}: {msg['content']}")
        print("-" * 60)
    
    def clear_history(self, device_prefix: str):
        """清除聊天历史"""
        if not device_prefix:
            print("用法: clear <设备ID前缀>")
            return
        
        # 查找设备
        device = None
        for d in self.app.device_manager.devices.values():
            if d.device_id.startswith(device_prefix.upper()):
                device = d
                break
        
        if not device:
            print(f"未找到ID以 '{device_prefix}' 开头的设备")
            return
        
        confirm = input(f"确定要清除与 {device.nickname} 的所有聊天记录吗? (y/n): ")
        if confirm.lower() == 'y':
            self.app.delete_chat_history(device.device_id)
            print("聊天记录已清除")
    
    def handle_group_command(self, args: str):
        """处理群组命令"""
        parts = args.split(maxsplit=1)
        if not parts:
            print("用法: group <create|list> [参数]")
            return
        
        subcmd = parts[0].lower()
        subargs = parts[1] if len(parts) > 1 else ""
        
        if subcmd == 'create':
            self.create_group(subargs)
        elif subcmd == 'list':
            self.list_groups()
        else:
            print(f"未知群组命令: {subcmd}")
    
    def create_group(self, args: str):
        """创建群组"""
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            print("用法: group create <群名称> <成员ID前缀1,成员ID前缀2,...>")
            return
        
        group_name, member_prefixes = parts
        prefixes = [p.strip().upper() for p in member_prefixes.split(',')]
        
        # 查找设备
        member_ids = []
        for prefix in prefixes:
            found = False
            for device in self.app.get_online_devices():
                if device.device_id.startswith(prefix):
                    member_ids.append(device.device_id)
                    found = True
                    break
            if not found:
                print(f"警告: 未找到ID以 '{prefix}' 开头的设备")
        
        if not member_ids:
            print("没有找到任何成员，无法创建群组")
            return
        
        group_id = self.app.create_group(group_name, member_ids)
        print(f"群组创建成功! 群ID: {group_id[:8]}...")
    
    def list_groups(self):
        """列出所有群组"""
        groups = self.app.get_groups()
        
        if not groups:
            print("当前没有群组")
            return
        
        print(f"\n群组列表 ({len(groups)}个):")
        print("-" * 60)
        for group in groups:
            print(f"  群名: {group['group_name']:20}  成员: {len(group['members'])}人")
        print("-" * 60)


def main():
    """主函数"""
    cli = TinyIMCLI()
    cli.start()


if __name__ == '__main__':
    main()
