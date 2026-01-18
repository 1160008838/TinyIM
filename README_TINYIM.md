# TinyIM - 局域网点对点即时通讯软件

## 项目概述

TinyIM 是一款无服务器、局域网内点对点的跨平台即时通讯软件，支持 Android、iOS、Windows 三大系统。无需注册登录，专注本地通讯与多端协同。

## 技术架构

### 跨平台方案
- **桌面端 (Windows/Linux)**: Python + PyQt6
- **移动端 (Android/iOS)**: Flutter 框架 (推荐) 或 React Native

### 核心技术栈
- **设备发现**: UDP 多播 (Multicast)
- **数据传输**: TCP (可靠传输) + UDP (实时通话)
- **本地存储**: SQLite
- **音视频**: WebRTC / PyAudio + OpenCV
- **UI 设计**: 参考微信风格

## 项目结构

```
TinyIM/
├── desktop/                 # 桌面端实现 (Python + PyQt6)
│   ├── src/
│   │   ├── core/           # 核心模块
│   │   │   ├── network/    # 网络通信
│   │   │   ├── device/     # 设备发现与管理
│   │   │   └── storage/    # 本地存储
│   │   ├── ui/             # 用户界面
│   │   └── utils/          # 工具类
│   ├── resources/          # 资源文件
│   ├── requirements.txt    # Python 依赖
│   └── main.py            # 入口文件
│
├── mobile_flutter/         # Flutter 移动端 (Android + iOS)
│   ├── lib/
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   ├── ui/            # 界面组件
│   │   └── main.dart      # 入口文件
│   └── pubspec.yaml       # Flutter 依赖
│
├── docs/                   # 文档
│   ├── architecture.md     # 架构设计
│   ├── api_protocol.md     # 通信协议
│   ├── build_guide.md      # 编译指南
│   └── user_manual.md      # 使用说明
│
└── README_TINYIM.md       # 本文件
```

## 核心功能

### 1. 设备发现与管理
- ✅ 自动扫描局域网设备
- ✅ 唯一设备 ID 生成
- ✅ 在线状态实时更新
- ✅ 自定义昵称和头像

### 2. 通讯功能
#### 单聊
- ✅ 文字消息
- ✅ 表情支持
- ✅ 图片分享
- ✅ 文件传输
- ✅ 语音消息
- ✅ 视频分享

#### 群聊
- ✅ 创建群组
- ✅ 成员管理
- ✅ 群公告
- ✅ @提醒功能

#### 音视频通话
- ✅ 语音通话
- ✅ 视频通话
- ✅ 视频会议

### 3. 本地存储
- ✅ 聊天历史记录
- ✅ 文件管理
- ✅ 自定义保存路径
- ✅ 记录删除

### 4. 个性化设置
- ✅ 个人信息设置
- ✅ 联系人备注
- ✅ 消息通知
- ✅ 多语言支持

## 性能指标

- 设备发现响应时间: ≤ 3 秒
- 消息发送延迟: ≤ 500ms
- 文件传输: 匹配局域网带宽上限
- 音视频通话延迟: ≤ 1 秒

## 快速开始

### 桌面端 (Windows/Linux)

```bash
# 1. 安装依赖
cd desktop
pip install -r requirements.txt

# 2. 运行程序
python main.py
```

### 移动端编译

参见 [docs/build_guide.md](docs/build_guide.md)

## 开发规范

### 代码规范
- 模块化设计，低耦合高内聚
- 关键函数添加详细注释
- 遵循 PEP 8 (Python) 和 Dart 官方规范

### 测试要求
- 单元测试覆盖核心模块
- 局域网环境集成测试
- 性能测试验证指标

## 兼容性

- **Android**: 8.0+ (API Level 26+)
- **iOS**: 12.0+
- **Windows**: 10+
- **Linux**: Ubuntu 18.04+

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 联系方式

项目主页: https://github.com/1160008838/TinyIM
