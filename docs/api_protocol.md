# TinyIM 通信协议文档

## 1. 协议概述

TinyIM 使用两种网络协议实现局域网点对点通信：

1. **UDP 多播** - 用于设备发现
2. **TCP** - 用于可靠的消息传输

## 2. 设备发现协议 (UDP Multicast)

### 2.1 基本参数

| 参数 | 值 |
|------|-----|
| 协议 | UDP |
| 多播地址 | 239.255.255.250 |
| 端口 | 5353 |
| 编码 | UTF-8 |
| 格式 | JSON |

### 2.2 消息类型

#### DISCOVER - 设备发现请求

发送方广播此消息以发现局域网内的其他设备。

```json
{
  "type": "DISCOVER",
  "device": {
    "device_id": "A1B2C3D4E5F6G7H8",
    "nickname": "小明的电脑",
    "ip_address": "192.168.1.100",
    "avatar_path": "default_avatar.png",
    "is_online": true
  }
}
```

#### RESPONSE - 发现响应

收到 DISCOVER 后，设备发送此响应。

```json
{
  "type": "RESPONSE",
  "device": {
    "device_id": "9I8H7G6F5E4D3C2B",
    "nickname": "小红的手机",
    "ip_address": "192.168.1.101",
    "avatar_path": "avatar_001.png",
    "is_online": true
  }
}
```

#### ANNOUNCE - 上线公告

设备定期（30秒）发送此消息宣告自己在线。

```json
{
  "type": "ANNOUNCE",
  "device": {
    "device_id": "A1B2C3D4E5F6G7H8",
    "nickname": "小明的电脑",
    "ip_address": "192.168.1.100",
    "avatar_path": "default_avatar.png",
    "is_online": true
  }
}
```

#### GOODBYE - 下线通知

设备正常退出时发送此消息。

```json
{
  "type": "GOODBYE",
  "device": {
    "device_id": "A1B2C3D4E5F6G7H8",
    "nickname": "小明的电脑",
    "ip_address": "192.168.1.100",
    "avatar_path": "default_avatar.png",
    "is_online": false
  }
}
```

### 2.3 设备发现流程

```
设备A                                设备B
  │                                    │
  ├── 启动，加入多播组                 │
  │                                    ├── 启动，加入多播组
  │                                    │
  ├── 发送 DISCOVER ──────────────────>│
  │                                    ├── 收到DISCOVER
  │                                    │
  │                   <─────────────── ├── 发送 RESPONSE
  ├── 收到RESPONSE                     │
  ├── 添加设备B到列表                  │
  │                                    │
  ├── 定期发送 ANNOUNCE (30秒)         ├── 定期发送 ANNOUNCE
  │                                    │
  ...                                 ...
  │                                    │
  ├── 退出时发送 GOODBYE               │
```

## 3. 消息传输协议 (TCP)

### 3.1 基本参数

| 参数 | 值 |
|------|-----|
| 协议 | TCP |
| 端口 | 9527 |
| 编码 | UTF-8 |
| 格式 | JSON |
| 超时 | 5 秒 |

### 3.2 消息帧格式

```
+-------------------+------------------------+----------+
| 消息长度 (4字节)  |  消息内容 (JSON)        | 确认(2字节)|
+-------------------+------------------------+----------+
|   Big Endian      |       UTF-8            |   "OK"   |
+-------------------+------------------------+----------+
```

**示例**:
```
[0, 0, 0, 150][{"msg_id": "...", ...}]["OK"]
```

### 3.3 消息对象结构

#### 基本消息字段

```json
{
  "msg_id": "uuid-v4-string",
  "sender_id": "发送者设备ID",
  "receiver_id": "接收者设备ID或群ID",
  "msg_type": "消息类型",
  "content": "消息内容（格式取决于类型）",
  "timestamp": "ISO 8601格式时间戳",
  "is_group": false,
  "is_read": false
}
```

#### 消息类型定义

##### 1. TEXT - 文字消息

```json
{
  "msg_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "sender_id": "A1B2C3D4E5F6G7H8",
  "receiver_id": "9I8H7G6F5E4D3C2B",
  "msg_type": "text",
  "content": "你好，这是一条文字消息",
  "timestamp": "2024-01-18T10:30:00.000Z",
  "is_group": false,
  "is_read": false
}
```

##### 2. IMAGE - 图片消息

```json
{
  "msg_id": "...",
  "msg_type": "image",
  "content": {
    "path": "/path/to/image.jpg",
    "width": 1920,
    "height": 1080,
    "size": 524288
  },
  ...
}
```

##### 3. FILE - 文件消息

```json
{
  "msg_id": "...",
  "msg_type": "file",
  "content": {
    "filename": "document.pdf",
    "filesize": 2097152,
    "path": "/path/to/document.pdf",
    "mime_type": "application/pdf"
  },
  ...
}
```

##### 4. VOICE - 语音消息

```json
{
  "msg_id": "...",
  "msg_type": "voice",
  "content": {
    "path": "/path/to/voice.mp3",
    "duration": 15,
    "format": "mp3"
  },
  ...
}
```

##### 5. VIDEO - 视频消息

```json
{
  "msg_id": "...",
  "msg_type": "video",
  "content": {
    "path": "/path/to/video.mp4",
    "duration": 60,
    "width": 1920,
    "height": 1080,
    "size": 10485760,
    "thumbnail": "/path/to/thumbnail.jpg"
  },
  ...
}
```

##### 6. EMOJI - 表情消息

```json
{
  "msg_id": "...",
  "msg_type": "emoji",
  "content": {
    "emoji_code": "😀",
    "emoji_id": "smile"
  },
  ...
}
```

##### 7. SYSTEM - 系统消息

```json
{
  "msg_id": "...",
  "msg_type": "system",
  "content": "小明加入了群聊",
  ...
}
```

##### 8. READ_RECEIPT - 已读回执

```json
{
  "msg_id": "...",
  "msg_type": "read_receipt",
  "content": {
    "original_msg_id": "原消息ID",
    "read_at": "2024-01-18T10:31:00.000Z"
  },
  ...
}
```

##### 9. RECALL - 撤回消息

```json
{
  "msg_id": "...",
  "msg_type": "recall",
  "content": {
    "original_msg_id": "要撤回的消息ID"
  },
  ...
}
```

### 3.4 TCP 传输流程

#### 单次消息传输

```
客户端                              服务端
  │                                    │
  ├── 建立TCP连接 ──────────────────> │
  │                                    ├── 接受连接
  │                                    │
  ├── 发送消息长度 (4字节) ──────────>│
  │                                    ├── 读取长度
  │                                    │
  ├── 发送消息JSON ──────────────────>│
  │                                    ├── 读取完整消息
  │                                    ├── 解析JSON
  │                                    ├── 保存到数据库
  │                                    │
  │                   <──────────────  ├── 返回 "OK"
  ├── 收到确认                         │
  │                                    │
  └── 关闭连接                         └── 关闭连接
```

#### 错误处理

| 错误类型 | 处理方式 |
|---------|----------|
| 连接超时 | 重试3次，间隔1秒 |
| 对方离线 | 标记为失败，稍后重试 |
| 数据损坏 | 返回错误，请求重发 |
| 端口被占用 | 使用备用端口 9528 |

## 4. 文件传输协议

### 4.1 小文件传输 (< 10MB)

小文件直接通过 TCP 消息发送：

1. 将文件内容 Base64 编码
2. 作为消息 content 发送
3. 接收方解码并保存

```json
{
  "msg_type": "file",
  "content": {
    "filename": "small_file.txt",
    "filesize": 5120,
    "data": "base64编码的文件内容..."
  }
}
```

### 4.2 大文件传输 (>= 10MB)

大文件使用分块传输：

#### 4.2.1 传输流程

```
发送方                              接收方
  │                                    │
  ├── 发送FILE_TRANSFER_START ───────>│
  │   (文件信息：名称、大小、MD5)      ├── 准备接收
  │                                    │
  ├── 建立文件传输TCP连接 ───────────>│
  │                                    │
  ├── 发送文件块1 (8KB) ─────────────>│
  │                                    ├── 写入缓冲
  ├── 发送文件块2 (8KB) ─────────────>│
  │                                    ├── 写入缓冲
  ...                                 ...
  │                                    │
  │                   <──────────────  ├── 每10块确认一次
  │                                    │
  ├── 发送最后一块 ──────────────────>│
  │                                    ├── 写入完成
  │                                    ├── 校验MD5
  │                   <──────────────  ├── 发送完成确认
  │                                    │
  └── 关闭连接                         └── 关闭连接
```

#### 4.2.2 文件传输消息

**FILE_TRANSFER_START**

```json
{
  "msg_type": "file_transfer_start",
  "content": {
    "transfer_id": "unique-transfer-id",
    "filename": "large_file.zip",
    "filesize": 104857600,
    "md5": "md5-hash-of-file",
    "chunk_size": 8192
  }
}
```

**FILE_TRANSFER_CHUNK**

二进制数据，格式：
```
[4字节: transfer_id长度][transfer_id][4字节: chunk序号][chunk数据]
```

**FILE_TRANSFER_COMPLETE**

```json
{
  "msg_type": "file_transfer_complete",
  "content": {
    "transfer_id": "unique-transfer-id",
    "status": "success",
    "md5": "接收后计算的MD5"
  }
}
```

### 4.3 断点续传

支持断点续传机制：

1. 接收方记录已接收的块号
2. 传输中断时，保存状态
3. 重新连接后发送 `FILE_TRANSFER_RESUME` 消息
4. 从上次中断处继续传输

```json
{
  "msg_type": "file_transfer_resume",
  "content": {
    "transfer_id": "unique-transfer-id",
    "last_chunk_received": 1250
  }
}
```

## 5. 群组协议

### 5.1 群组操作消息

#### GROUP_CREATE - 创建群组

```json
{
  "msg_type": "group_create",
  "content": {
    "group_id": "group-uuid",
    "group_name": "我的朋友们",
    "creator_id": "A1B2C3D4E5F6G7H8",
    "members": ["device_id1", "device_id2", "device_id3"]
  }
}
```

#### GROUP_INVITE - 邀请加入群组

```json
{
  "msg_type": "group_invite",
  "content": {
    "group_id": "group-uuid",
    "inviter_id": "A1B2C3D4E5F6G7H8",
    "invitee_id": "new-member-id"
  }
}
```

#### GROUP_REMOVE - 移除群成员

```json
{
  "msg_type": "group_remove",
  "content": {
    "group_id": "group-uuid",
    "operator_id": "creator-id",
    "removed_id": "member-to-remove"
  }
}
```

#### GROUP_LEAVE - 退出群组

```json
{
  "msg_type": "group_leave",
  "content": {
    "group_id": "group-uuid",
    "member_id": "leaving-member-id"
  }
}
```

### 5.2 群消息分发

群消息由发送者分别发送给每个成员：

```
发送者                    成员1    成员2    成员3
  │                        │        │        │
  ├── 获取群成员列表       │        │        │
  │                        │        │        │
  ├── 发送给成员1 ────────>│        │        │
  ├── 发送给成员2 ───────────────>  │        │
  ├── 发送给成员3 ────────────────────────> │
```

## 6. 实时通话协议 (未来实现)

### 6.1 信令协议 (TCP)

#### CALL_REQUEST - 发起通话

```json
{
  "msg_type": "call_request",
  "content": {
    "call_id": "call-uuid",
    "caller_id": "A1B2C3D4E5F6G7H8",
    "callee_id": "9I8H7G6F5E4D3C2B",
    "call_type": "voice|video"
  }
}
```

#### CALL_ACCEPT - 接受通话

```json
{
  "msg_type": "call_accept",
  "content": {
    "call_id": "call-uuid"
  }
}
```

#### CALL_REJECT - 拒绝通话

```json
{
  "msg_type": "call_reject",
  "content": {
    "call_id": "call-uuid",
    "reason": "busy|declined"
  }
}
```

#### CALL_END - 结束通话

```json
{
  "msg_type": "call_end",
  "content": {
    "call_id": "call-uuid",
    "duration": 125
  }
}
```

### 6.2 媒体流协议 (UDP)

使用 RTP (Real-time Transport Protocol) 传输音视频数据。

**端口分配**:
- 音频: UDP 10000-10099
- 视频: UDP 10100-10199

## 7. 协议版本控制

### 7.1 版本标识

所有消息包含版本字段：

```json
{
  "protocol_version": "1.0",
  "msg_id": "...",
  ...
}
```

### 7.2 兼容性

- 主版本号变化：不兼容
- 次版本号变化：向下兼容
- 修订版本号：完全兼容

## 8. 安全性考虑

### 8.1 当前安全措施

1. **设备ID验证**: 防止ID欺骗
2. **消息完整性**: JSON格式验证
3. **局域网隔离**: 外部无法访问

### 8.2 可选安全措施

1. **端到端加密**:
   - 使用 RSA-2048 交换密钥
   - 使用 AES-256 加密消息内容

2. **数字签名**:
   - 使用私钥签名消息
   - 接收方验证签名

3. **访问控制**:
   - 白名单机制
   - 黑名单机制

## 9. 性能优化

### 9.1 消息压缩

大于1KB的消息使用gzip压缩：

```
未压缩消息 -> gzip压缩 -> Base64编码 -> 发送
```

### 9.2 批量发送

多条消息合并发送：

```json
{
  "msg_type": "batch",
  "content": {
    "messages": [
      {...},
      {...},
      {...}
    ]
  }
}
```

### 9.3 连接复用

保持TCP连接活跃，避免频繁建立连接。

## 10. 错误码定义

| 错误码 | 说明 |
|-------|------|
| 200 | 成功 |
| 400 | 请求格式错误 |
| 401 | 设备未授权 |
| 404 | 目标设备不存在 |
| 408 | 请求超时 |
| 413 | 消息过大 |
| 500 | 内部错误 |
| 503 | 服务不可用 |
