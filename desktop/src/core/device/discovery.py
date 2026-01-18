"""
设备发现模块
使用UDP多播进行局域网设备发现
"""
import socket
import json
import threading
import time
from typing import Callable, Optional


class DeviceDiscovery:
    """设备发现服务"""
    
    # 多播地址和端口
    MULTICAST_GROUP = '239.255.255.250'
    MULTICAST_PORT = 5353
    
    # 消息类型
    MSG_ANNOUNCE = 'ANNOUNCE'      # 设备上线公告
    MSG_DISCOVER = 'DISCOVER'      # 发现请求
    MSG_RESPONSE = 'RESPONSE'      # 发现响应
    MSG_GOODBYE = 'GOODBYE'        # 设备下线
    
    def __init__(self, device_info, callback: Optional[Callable] = None):
        """
        初始化设备发现服务
        
        Args:
            device_info: 本地设备信息
            callback: 发现设备时的回调函数
        """
        self.device_info = device_info
        self.callback = callback
        self.running = False
        self.sock = None
        self.listen_thread = None
        self.announce_thread = None
        
    def start(self):
        """启动设备发现服务"""
        if self.running:
            return
            
        self.running = True
        
        # 创建UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 绑定到多播端口
        self.sock.bind(('', self.MULTICAST_PORT))
        
        # 加入多播组
        mreq = socket.inet_aton(self.MULTICAST_GROUP) + socket.inet_aton('0.0.0.0')
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        # 启动监听线程
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        # 启动定期公告线程
        self.announce_thread = threading.Thread(target=self._announce_loop, daemon=True)
        self.announce_thread.start()
        
        # 发送初始发现请求
        self.send_discover()
        
    def stop(self):
        """停止设备发现服务"""
        if not self.running:
            return
            
        self.running = False
        
        # 发送下线消息
        self.send_goodbye()
        
        # 关闭socket
        if self.sock:
            self.sock.close()
            
        # 等待线程结束
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        if self.announce_thread:
            self.announce_thread.join(timeout=2)
    
    def _listen_loop(self):
        """监听循环，接收多播消息"""
        while self.running:
            try:
                self.sock.settimeout(1.0)
                data, addr = self.sock.recvfrom(4096)
                
                # 解析消息
                try:
                    message = json.loads(data.decode('utf-8'))
                    self._handle_message(message, addr)
                except json.JSONDecodeError:
                    pass  # 忽略无效消息
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:  # 只在运行时打印错误
                    print(f"Discovery listen error: {e}")
    
    def _announce_loop(self):
        """定期公告循环"""
        while self.running:
            self.send_announce()
            time.sleep(30)  # 每30秒公告一次
    
    def _handle_message(self, message: dict, addr: tuple):
        """
        处理接收到的消息
        
        Args:
            message: 消息内容
            addr: 发送者地址
        """
        msg_type = message.get('type')
        device_data = message.get('device')
        
        # 忽略自己发送的消息
        if device_data and device_data.get('device_id') == self.device_info.device_id:
            return
        
        if msg_type == self.MSG_DISCOVER:
            # 收到发现请求，发送响应
            self.send_response()
            
        elif msg_type in [self.MSG_ANNOUNCE, self.MSG_RESPONSE]:
            # 收到设备公告或响应
            if self.callback and device_data:
                device_data['is_online'] = True
                self.callback('device_found', device_data)
                
        elif msg_type == self.MSG_GOODBYE:
            # 收到下线消息
            if self.callback and device_data:
                device_data['is_online'] = False
                self.callback('device_left', device_data)
    
    def _send_message(self, msg_type: str):
        """
        发送消息
        
        Args:
            msg_type: 消息类型
        """
        message = {
            'type': msg_type,
            'device': self.device_info.to_dict()
        }
        
        try:
            data = json.dumps(message).encode('utf-8')
            self.sock.sendto(data, (self.MULTICAST_GROUP, self.MULTICAST_PORT))
        except Exception as e:
            print(f"Send message error: {e}")
    
    def send_discover(self):
        """发送设备发现请求"""
        self._send_message(self.MSG_DISCOVER)
    
    def send_announce(self):
        """发送设备上线公告"""
        self._send_message(self.MSG_ANNOUNCE)
    
    def send_response(self):
        """发送发现响应"""
        self._send_message(self.MSG_RESPONSE)
    
    def send_goodbye(self):
        """发送设备下线消息"""
        self._send_message(self.MSG_GOODBYE)
