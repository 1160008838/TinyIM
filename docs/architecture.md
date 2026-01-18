# TinyIM 架构设计文档

## 1. 系统架构概览

TinyIM 采用**点对点（P2P）无中心服务器架构**，所有设备在局域网内地位平等，直接进行通信。

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     TinyIM Application                   │
├─────────────────────────────────────────────────────────┤
│  UI Layer                                                │
│  ├── PyQt6 Desktop UI (Windows/Linux)                   │
│  └── Flutter UI (Android/iOS)                           │
├─────────────────────────────────────────────────────────┤
│  Application Logic Layer                                │
│  └── TinyIMApp (Controller)                            │
├─────────────────────────────────────────────────────────┤
│  Core Modules                                            │
│  ├── Device Module                                      │
│  │   ├── DeviceManager (设备管理)                      │
│  │   └── DeviceDiscovery (设备发现)                    │
│  ├── Network Module                                     │
│  │   ├── TCPServer/Client (可靠传输)                   │
│  │   ├── MessageQueue (消息队列)                       │
│  │   └── Message (消息模型)                            │
│  └── Storage Module                                     │
│      └── Database (SQLite 本地存储)                    │
└─────────────────────────────────────────────────────────┘
```

## 2. 核心模块详细设计

### 2.1 设备发现模块 (Device Discovery)

#### 2.1.1 设备发现流程

```
设备A启动                          设备B启动
   │                                  │
   ├─ 生成唯一设备ID                  ├─ 生成唯一设备ID
   │                                  │
   ├─ 加入多播组 239.255.255.250      ├─ 加入多播组
   │                                  │
   ├─ 发送 DISCOVER 广播 ────────────>│
   │                                  ├─ 收到DISCOVER
   │                 <─────────────── ├─ 发送 RESPONSE
   ├─ 收到RESPONSE                    │
   ├─ 添加设备B到列表                 │
   │                                  │
   ├─ 定期发送 ANNOUNCE (30秒)        ├─ 定期发送 ANNOUNCE
   │                                  │
   ├─ 下线时发送 GOODBYE              │
```

#### 2.1.2 设备ID生成算法

```python
device_id = SHA256(MAC地址 + 主机名 + 系统信息)[:16]
```

**特点**:
- 基于硬件信息，同一设备ID保持一致
- 16位十六进制，确保唯一性
- 局域网内不同设备ID碰撞概率极低

#### 2.1.3 多播协议

- **多播地址**: 239.255.255.250
- **端口**: 5353
- **消息格式**: JSON

```json
{
  "type": "ANNOUNCE|DISCOVER|RESPONSE|GOODBYE",
  "device": {
    "device_id": "A1B2C3D4E5F6G7H8",
    "nickname": "小明的电脑",
    "ip_address": "192.168.1.100",
    "avatar_path": "default_avatar.png",
    "is_online": true
  }
}
```

### 2.2 网络通信模块 (Network Communication)

#### 2.2.1 TCP通信协议

采用**TCP**进行可靠的点对点消息传输。

**消息传输格式**:
```
[4字节消息长度][JSON消息内容][确认字节]
```

**流程**:
```
发送端                              接收端
   │                                  │
   ├─ 连接目标IP:9527 ──────────────>│
   │                                  ├─ 接受连接
   ├─ 发送消息长度(4字节) ──────────>│
   │                                  ├─ 读取长度
   ├─ 发送消息内容(JSON) ───────────>│
   │                                  ├─ 读取完整消息
   │                                  ├─ 解析JSON
   │                 <──────────────  ├─ 返回"OK"确认
   ├─ 收到确认                        │
   └─ 关闭连接                        └─ 关闭连接
```

#### 2.2.2 消息类型定义

| 类型 | 说明 | content格式 |
|------|------|-------------|
| TEXT | 文字消息 | string |
| IMAGE | 图片消息 | {"path": "..."} |
| FILE | 文件消息 | {"filename": "...", "filesize": ..., "path": "..."} |
| VOICE | 语音消息 | {"path": "...", "duration": ...} |
| VIDEO | 视频消息 | {"path": "...", "duration": ...} |
| EMOJI | 表情消息 | {"emoji_code": "..."} |
| SYSTEM | 系统消息 | string |

#### 2.2.3 消息队列

为避免网络阻塞，采用**异步消息队列**:

```
主线程                    队列线程
   │                        │
   ├─ enqueue(msg) ────────>│
   │                        ├─ 从队列取出
   │                        ├─ TCP发送
   │                        │   └─ 重试3次
   │                        └─ 继续处理下一条
   │
```

### 2.3 本地存储模块 (Storage)

#### 2.3.1 数据库表结构

**devices 表** - 设备信息
```sql
CREATE TABLE devices (
    device_id TEXT PRIMARY KEY,
    nickname TEXT NOT NULL,
    ip_address TEXT,
    avatar_path TEXT,
    remark TEXT,              -- 备注名
    last_seen TEXT,
    created_at TEXT
)
```

**messages 表** - 消息记录
```sql
CREATE TABLE messages (
    msg_id TEXT PRIMARY KEY,
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    msg_type TEXT NOT NULL,
    content TEXT,
    timestamp TEXT NOT NULL,
    is_group INTEGER DEFAULT 0,
    is_read INTEGER DEFAULT 0,
    created_at TEXT
)
```

**groups 表** - 群组信息
```sql
CREATE TABLE groups (
    group_id TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    creator_id TEXT NOT NULL,
    announcement TEXT,
    created_at TEXT
)
```

**group_members 表** - 群成员
```sql
CREATE TABLE group_members (
    group_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    joined_at TEXT,
    PRIMARY KEY (group_id, device_id)
)
```

**settings 表** - 应用设置
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TEXT
)
```

## 3. 功能实现设计

### 3.1 单聊实现

```
用户A                 TinyIM App              用户B
  │                       │                      │
  ├─ 输入消息 "你好"      │                      │
  │                       │                      │
  ├─ send_text() ────────>│                      │
  │                       ├─ 创建Message对象     │
  │                       ├─ 保存到本地数据库    │
  │                       ├─ 查找设备B的IP       │
  │                       ├─ TCP发送 ───────────>│
  │                       │                      ├─ 接收消息
  │                       │                      ├─ 保存到数据库
  │                       │                      ├─ UI显示
  │                       │                      │
```

### 3.2 群聊实现

群聊采用**消息分发**模式：

```
发送者                                    接收者1/2/3
  │                                           │
  ├─ 发送群消息                               │
  │                                           │
  ├─ 获取群成员列表 [成员1, 成员2, 成员3]     │
  │                                           │
  ├─ 依次发送给每个成员 ────────────────────>│ 成员1收到
  ├─ 发送给成员2 ────────────────────────────>│ 成员2收到
  ├─ 发送给成员3 ────────────────────────────>│ 成员3收到
  │                                           │
```

### 3.3 文件传输实现

文件传输仍使用TCP，但采用**分块传输**:

```
发送端                              接收端
   │                                  │
   ├─ 发送FILE消息                    │
   │  (包含文件名、大小、元信息)      ├─ 创建接收任务
   │                                  │
   ├─ 建立文件传输连接 ──────────────>│
   │                                  │
   ├─ 分块发送文件数据                │
   │  (每块8KB) ───────────────────>│
   │             ───────────────────>│
   │             ───────────────────>│
   │                                  ├─ 写入本地文件
   │                                  ├─ 更新进度
   │                 <──────────────  │
   │                                  ├─ 发送完成确认
   └─ 传输完成                        └─ 通知用户
```

### 3.4 语音/视频通话实现 (未来扩展)

采用 **WebRTC** 或 **UDP + RTP** 协议:

```
呼叫方                              接听方
   │                                  │
   ├─ 发送CALL_REQUEST ─────────────>│
   │                                  ├─ 显示来电界面
   │                                  │
   │                 <──────────────  ├─ 发送CALL_ACCEPT
   │                                  │
   ├─ 建立P2P连接(STUN/TURN)          │
   │  <────────────────────────────> │
   │                                  │
   ├─ 实时音视频流(UDP) <──────────> │
   │                                  │
```

## 4. 性能优化设计

### 4.1 设备发现优化

- 使用UDP多播降低网络开销
- 定期公告间隔30秒，减少广播频率
- 超时检测：60秒无响应标记为离线

### 4.2 消息传输优化

- 异步消息队列，避免阻塞主线程
- TCP连接超时5秒，快速失败
- 消息重试机制（最多3次）

### 4.3 数据库优化

- 为常用字段建立索引
- 消息历史分页加载（默认50条）
- 定期清理过期数据

### 4.4 图片压缩

- 发送前自动压缩（质量85%）
- 限制最大尺寸（1920x1080）
- 生成缩略图用于列表显示

## 5. 安全性设计

### 5.1 基础安全

- 局域网内通信，外部无法访问
- 设备ID唯一性验证
- 消息来源验证

### 5.2 扩展安全 (可选)

- **端到端加密**: 使用RSA或AES加密消息内容
- **数字签名**: 验证消息完整性和发送者身份
- **访问控制**: 设置允许/拒绝通信的设备列表

## 6. 跨平台实现方案

### 6.1 桌面端 (Windows/Linux)

- **框架**: Python + PyQt6
- **网络**: Python socket
- **存储**: SQLite3
- **打包**: PyInstaller

### 6.2 移动端 (Android/iOS)

- **框架**: Flutter
- **网络**: Dart socket/UDP
- **存储**: sqflite
- **打包**: flutter build apk/ipa

### 6.3 代码复用

- 核心网络协议一致
- 消息格式统一（JSON）
- 数据库结构相同
- 业务逻辑相似

## 7. 扩展性设计

### 7.1 插件式架构

```python
class Plugin:
    def on_message(self, message):
        pass
    
    def on_device_event(self, event, device):
        pass

# 注册插件
app.register_plugin(MyPlugin())
```

### 7.2 预留接口

- 消息类型可扩展
- 自定义表情包支持
- 屏幕共享接口
- 文件同步接口

## 8. 测试策略

### 8.1 单元测试

- 设备ID生成唯一性
- 消息序列化/反序列化
- 数据库CRUD操作

### 8.2 集成测试

- 设备发现功能
- 点对点消息传输
- 群组消息分发

### 8.3 性能测试

- 1000条消息发送耗时
- 100MB文件传输速度
- 10个设备同时在线

### 8.4 兼容性测试

- 不同操作系统互通
- 不同网络环境（WiFi/有线）
- 多版本共存
