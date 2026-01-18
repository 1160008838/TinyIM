"""
TCP通信模块
负责点对点消息传输
"""
import socket
import json
import threading
from typing import Callable, Optional
from queue import Queue


class TCPServer:
    """TCP服务器，用于接收消息"""
    
    PORT = 9527  # 监听端口
    
    def __init__(self, callback: Optional[Callable] = None):
        """
        初始化TCP服务器
        
        Args:
            callback: 接收消息的回调函数
        """
        self.callback = callback
        self.running = False
        self.server_socket = None
        self.accept_thread = None
        self.client_threads = []
        
    def start(self):
        """启动服务器"""
        if self.running:
            return
            
        self.running = True
        
        # 创建服务器socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.PORT))
        self.server_socket.listen(10)
        
        # 启动接受连接的线程
        self.accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self.accept_thread.start()
        
        print(f"TCP Server started on port {self.PORT}")
    
    def stop(self):
        """停止服务器"""
        if not self.running:
            return
            
        self.running = False
        
        # 关闭服务器socket
        if self.server_socket:
            self.server_socket.close()
        
        # 等待线程结束
        if self.accept_thread:
            self.accept_thread.join(timeout=2)
    
    def _accept_loop(self):
        """接受连接循环"""
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                client_socket, addr = self.server_socket.accept()
                
                # 为每个客户端创建处理线程
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, addr),
                    daemon=True
                )
                client_thread.start()
                self.client_threads.append(client_thread)
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Accept error: {e}")
    
    def _handle_client(self, client_socket: socket.socket, addr: tuple):
        """
        处理客户端连接
        
        Args:
            client_socket: 客户端socket
            addr: 客户端地址
        """
        try:
            # 接收数据长度（前4字节）
            length_data = self._recv_all(client_socket, 4)
            if not length_data:
                return
            
            msg_length = int.from_bytes(length_data, byteorder='big')
            
            # 接收完整消息
            msg_data = self._recv_all(client_socket, msg_length)
            if not msg_data:
                return
            
            # 解析消息
            message_dict = json.loads(msg_data.decode('utf-8'))
            
            # 调用回调函数
            if self.callback:
                self.callback(message_dict)
            
            # 发送确认
            client_socket.sendall(b'OK')
            
        except Exception as e:
            print(f"Handle client error: {e}")
        finally:
            client_socket.close()
    
    def _recv_all(self, sock: socket.socket, length: int) -> bytes:
        """
        接收指定长度的数据
        
        Args:
            sock: socket对象
            length: 数据长度
            
        Returns:
            bytes: 接收到的数据
        """
        data = b''
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                return None
            data += chunk
        return data


class TCPClient:
    """TCP客户端，用于发送消息"""
    
    PORT = 9527
    TIMEOUT = 5  # 连接超时时间（秒）
    
    @staticmethod
    def send_message(target_ip: str, message_dict: dict) -> bool:
        """
        发送消息到目标设备
        
        Args:
            target_ip: 目标IP地址
            message_dict: 消息字典
            
        Returns:
            bool: 是否发送成功
        """
        try:
            # 创建socket并连接
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(TCPClient.TIMEOUT)
            client_socket.connect((target_ip, TCPClient.PORT))
            
            # 将消息转为JSON
            msg_data = json.dumps(message_dict).encode('utf-8')
            msg_length = len(msg_data)
            
            # 发送消息长度（4字节）
            client_socket.sendall(msg_length.to_bytes(4, byteorder='big'))
            
            # 发送消息内容
            client_socket.sendall(msg_data)
            
            # 等待确认
            response = client_socket.recv(1024)
            
            client_socket.close()
            
            return response == b'OK'
            
        except Exception as e:
            print(f"Send message error to {target_ip}: {e}")
            return False


class MessageQueue:
    """消息队列，用于异步发送消息"""
    
    def __init__(self):
        self.queue = Queue()
        self.running = False
        self.worker_thread = None
    
    def start(self):
        """启动消息队列"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """停止消息队列"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
    
    def enqueue(self, target_ip: str, message_dict: dict):
        """
        将消息加入队列
        
        Args:
            target_ip: 目标IP
            message_dict: 消息字典
        """
        self.queue.put((target_ip, message_dict))
    
    def _worker(self):
        """工作线程，处理队列中的消息"""
        while self.running:
            try:
                if not self.queue.empty():
                    target_ip, message_dict = self.queue.get(timeout=1)
                    TCPClient.send_message(target_ip, message_dict)
            except Exception as e:
                print(f"Message queue worker error: {e}")
