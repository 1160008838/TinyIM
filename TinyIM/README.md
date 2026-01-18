# TinyIM - 局域网 P2P 通讯软件

基于 .NET MAUI 构建的跨平台局域网 P2P 通讯应用程序。

## 功能特性

### 1. 信息 (Messages)
- 自动发现局域网内的所有设备
- 显示设备信息：
  - 设备名称
  - 设备头像
  - 平台类型 (Windows, Android, iOS, Mac)
  - IP 地址
  - 在线状态

### 2. 应用 (Applications)
- 宫格布局展示可用应用
- 每行显示 4 个应用
- 包含的应用功能：
  - 文件传输
  - 屏幕共享
  - 远程桌面
  - 即时聊天
  - 语音通话
  - 视频通话
  - 剪贴板共享
  - 通知同步
  - 文件浏览
  - 相册共享
  - 音乐共享
  - 视频共享

### 3. 设置 (Settings)
- **个人信息**
  - 用户名称设置
  - 设备名称设置
  - 头像管理（待实现）
- **网络设置**
  - 自动发现开关
  - 发现端口配置
  - 网络接口选择
- **存储设置**
  - 下载路径配置
  - 自动清理设置
  - 最大存储空间限制

## 技术架构

### 项目结构
```
TinyIM/
├── Models/              # 数据模型
│   ├── Device.cs       # 设备模型
│   ├── AppItem.cs      # 应用项模型
│   └── UserSettings.cs # 用户设置模型
├── Views/              # 视图页面
│   ├── MessagesPage.xaml
│   ├── ApplicationsPage.xaml
│   └── SettingsPage.xaml
├── ViewModels/         # 视图模型
│   ├── MessagesViewModel.cs
│   ├── ApplicationsViewModel.cs
│   └── SettingsViewModel.cs
├── Services/           # 服务层
│   └── DeviceDiscoveryService.cs
├── Converters/         # 数据转换器
│   └── BoolToColorConverter.cs
└── Resources/          # 资源文件
    ├── AppIcon/
    ├── Images/
    ├── Fonts/
    └── Styles/
```

### 技术栈
- **.NET 10.0**
- **MAUI (Multi-platform App UI)**
- **MVVM 架构模式**
- **XAML UI 设计**

## 开发环境要求

### 必需工具
- .NET 10.0 SDK 或更高版本
- MAUI workload

### 安装 MAUI Workload
```bash
dotnet workload install maui-android
# 或针对其他平台
dotnet workload install maui-ios
dotnet workload install maui-windows
```

## 构建和运行

### 还原依赖
```bash
cd TinyIM
dotnet restore
```

### 构建项目
```bash
dotnet build
```

### 运行应用（Android）
```bash
dotnet build -t:Run -f net10.0-android
```

### 运行应用（Windows）
```bash
dotnet build -t:Run -f net10.0-windows10.0.19041.0
```

### 运行应用（iOS/Mac）
```bash
dotnet build -t:Run -f net10.0-ios
# 或
dotnet build -t:Run -f net10.0-maccatalyst
```

## 支持的平台

- ✅ Android 5.0 (API 21) 及更高版本
- ✅ iOS 15.0 及更高版本
- ✅ macOS 12.0 及更高版本 (Mac Catalyst)
- ✅ Windows 10 版本 1809 及更高版本

## 当前实现状态

### 已完成 ✅
- [x] 基础项目结构
- [x] 三个主要页面的 UI 设计
- [x] MVVM 架构实现
- [x] 设备列表展示（模拟数据）
- [x] 应用网格布局（4列）
- [x] 设置页面表单
- [x] 底部导航栏
- [x] 数据绑定和状态管理

### 待实现 🚧
- [ ] 实际的 UDP 广播/多播设备发现
- [ ] P2P 网络通信协议
- [ ] 文件传输功能
- [ ] 实时聊天功能
- [ ] 屏幕共享功能
- [ ] 音视频通话功能
- [ ] 设置数据持久化
- [ ] 用户头像上传和显示
- [ ] 应用图标自定义
- [ ] 安全加密通信

## 代码说明

### 设备发现服务
`DeviceDiscoveryService` 是一个单例服务，负责：
- 管理局域网内发现的设备列表
- 提供设备发现和停止发现的接口
- 当前使用模拟数据进行演示

### 数据模型
- **LanDevice**: 表示局域网内的设备，包含名称、头像、平台、IP 地址等信息
- **AppItem**: 表示应用项目，包含名称、图标和描述
- **UserSettings**: 用户设置，包含个人信息、网络设置和存储设置

### 视图模型
使用 MVVM 模式，每个页面都有对应的 ViewModel：
- **MessagesViewModel**: 管理设备列表数据
- **ApplicationsViewModel**: 管理应用列表数据
- **SettingsViewModel**: 管理设置数据和保存逻辑

## 配置说明

### 修改目标平台
编辑 `TinyIM.csproj` 文件中的 `TargetFrameworks` 属性：
```xml
<TargetFrameworks>net10.0-android;net10.0-ios;net10.0-maccatalyst;net10.0-windows10.0.19041.0</TargetFrameworks>
```

### 默认端口
- 设备发现端口: `8888`
- 可在设置页面中修改

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。
