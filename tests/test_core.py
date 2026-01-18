#!/usr/bin/env python3
"""
TinyIM 测试脚本
测试核心功能模块
"""
import sys
import os
import time

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../desktop/src'))

from core.device import DeviceInfo, DeviceManager, DeviceDiscovery
from core.network import Message, MessageType, TCPServer, TCPClient
from core.storage import Database


def test_device_id_generation():
    """测试设备ID生成的唯一性"""
    print("=" * 60)
    print("测试: 设备ID生成")
    print("-" * 60)
    
    device1 = DeviceInfo()
    device2 = DeviceInfo()
    
    print(f"设备1 ID: {device1.device_id}")
    print(f"设备2 ID: {device2.device_id}")
    
    # 同一设备应该生成相同的ID
    assert device1.device_id == device2.device_id, "设备ID应该一致"
    print("✓ 设备ID生成测试通过")
    print()


def test_message_serialization():
    """测试消息序列化和反序列化"""
    print("=" * 60)
    print("测试: 消息序列化")
    print("-" * 60)
    
    # 创建消息
    msg = Message(
        sender_id="SENDER123",
        receiver_id="RECEIVER456",
        msg_type=MessageType.TEXT,
        content="测试消息"
    )
    
    print(f"原始消息: {msg}")
    
    # 转为字典
    msg_dict = msg.to_dict()
    print(f"序列化: {msg_dict}")
    
    # 从字典恢复
    msg_restored = Message.from_dict(msg_dict)
    print(f"反序列化: {msg_restored}")
    
    # 验证
    assert msg.msg_id == msg_restored.msg_id
    assert msg.sender_id == msg_restored.sender_id
    assert msg.receiver_id == msg_restored.receiver_id
    assert msg.msg_type == msg_restored.msg_type
    assert msg.content == msg_restored.content
    
    print("✓ 消息序列化测试通过")
    print()


def test_database_operations():
    """测试数据库操作"""
    print("=" * 60)
    print("测试: 数据库操作")
    print("-" * 60)
    
    # 使用临时数据库
    import tempfile
    db_path = tempfile.mktemp(suffix='.db')
    
    db = Database(db_path)
    
    # 测试保存设备
    device_info = {
        'device_id': 'TEST123',
        'nickname': '测试设备',
        'ip_address': '192.168.1.100'
    }
    db.save_device(device_info)
    print("✓ 保存设备成功")
    
    # 测试读取设备
    retrieved = db.get_device('TEST123')
    assert retrieved is not None
    assert retrieved['nickname'] == '测试设备'
    print("✓ 读取设备成功")
    
    # 测试保存消息
    message = {
        'msg_id': 'MSG001',
        'sender_id': 'SENDER123',
        'receiver_id': 'RECEIVER456',
        'msg_type': 'text',
        'content': '测试消息内容',
        'timestamp': '2024-01-18T10:00:00',
        'is_group': False,
        'is_read': False
    }
    db.save_message(message)
    print("✓ 保存消息成功")
    
    # 测试读取消息
    messages = db.get_messages('RECEIVER456')
    assert len(messages) > 0
    assert messages[0]['content'] == '测试消息内容'
    print("✓ 读取消息成功")
    
    # 清理
    db.close()
    os.remove(db_path)
    
    print("✓ 数据库操作测试通过")
    print()


def test_tcp_communication():
    """测试TCP通信"""
    print("=" * 60)
    print("测试: TCP通信")
    print("-" * 60)
    
    received_messages = []
    
    def message_callback(msg_dict):
        received_messages.append(msg_dict)
        print(f"✓ 接收到消息: {msg_dict.get('content', '')}")
    
    # 启动服务器
    server = TCPServer(callback=message_callback)
    server.start()
    print("✓ TCP服务器启动")
    
    # 等待服务器准备好
    time.sleep(1)
    
    # 发送消息
    test_message = {
        'msg_id': 'TEST001',
        'sender_id': 'SENDER',
        'receiver_id': 'RECEIVER',
        'msg_type': 'text',
        'content': 'TCP测试消息',
        'timestamp': '2024-01-18T10:00:00',
        'is_group': False,
        'is_read': False
    }
    
    # 发送到本地
    success = TCPClient.send_message('127.0.0.1', test_message)
    print(f"✓ 发送消息: {'成功' if success else '失败'}")
    
    # 等待接收
    time.sleep(1)
    
    # 验证
    assert len(received_messages) > 0, "应该接收到消息"
    assert received_messages[0]['content'] == 'TCP测试消息'
    
    # 停止服务器
    server.stop()
    print("✓ TCP服务器停止")
    
    print("✓ TCP通信测试通过")
    print()


def test_device_discovery():
    """测试设备发现（需要手动验证）"""
    print("=" * 60)
    print("测试: 设备发现")
    print("-" * 60)
    print("注意: 此测试需要在局域网环境中运行")
    print("建议在多台设备上同时运行以测试发现功能")
    print()
    
    device = DeviceInfo()
    device.nickname = "测试设备"
    
    discovered_devices = []
    
    def discovery_callback(event_type, device_data):
        if event_type == 'device_found':
            discovered_devices.append(device_data)
            print(f"✓ 发现设备: {device_data['nickname']} ({device_data['ip_address']})")
    
    discovery = DeviceDiscovery(device, callback=discovery_callback)
    discovery.start()
    print("✓ 设备发现服务启动")
    
    # 运行10秒
    print("正在扫描局域网设备 (10秒)...")
    for i in range(10):
        time.sleep(1)
        print(f"  {i+1}/10 秒...")
    
    discovery.stop()
    print("✓ 设备发现服务停止")
    
    print(f"共发现 {len(discovered_devices)} 个设备")
    print()


def run_all_tests():
    """运行所有测试"""
    print()
    print("█" * 60)
    print(" " * 15 + "TinyIM 功能测试")
    print("█" * 60)
    print()
    
    try:
        test_device_id_generation()
        test_message_serialization()
        test_database_operations()
        test_tcp_communication()
        test_device_discovery()
        
        print("=" * 60)
        print("✓ 所有测试完成")
        print("=" * 60)
        print()
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    run_all_tests()
