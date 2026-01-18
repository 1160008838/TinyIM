# TinyIM Flutter 移动端

这是 TinyIM 的 Flutter 移动端实现，支持 Android 和 iOS 平台。

## 开发环境要求

- Flutter SDK 3.0.0 或更高版本
- Dart SDK 3.0.0 或更高版本
- Android Studio (Android 开发)
- Xcode (iOS 开发，仅 macOS)

## 快速开始

### 1. 安装依赖

```bash
flutter pub get
```

### 2. 运行应用

```bash
# 运行在 Android 设备/模拟器
flutter run

# 运行在 iOS 设备/模拟器 (仅 macOS)
flutter run -d ios

# 热重载: r
# 热重启: R
# 退出: q
```

### 3. 编译发布版本

```bash
# Android APK
flutter build apk --release

# Android App Bundle (推荐上传到 Google Play)
flutter build appbundle --release

# iOS (仅 macOS)
flutter build ios --release
```

## 项目结构

```
lib/
├── main.dart              # 应用入口
├── models/               # 数据模型
│   ├── device_info.dart  # 设备信息
│   └── message.dart      # 消息
├── services/             # 业务逻辑
│   └── app_service.dart  # 应用主服务
└── screens/              # 界面
    ├── home_screen.dart      # 主屏幕（底部导航）
    ├── contacts_screen.dart  # 联系人列表
    ├── chats_screen.dart     # 聊天列表
    ├── meetings_screen.dart  # 视频会议
    └── profile_screen.dart   # 个人资料
```

## 功能实现状态

### ✅ 已完成
- [x] 项目结构搭建
- [x] 底部导航界面
- [x] 基础数据模型
- [x] 状态管理框架

### 🚧 进行中
- [ ] UDP 多播设备发现
- [ ] TCP 消息收发
- [ ] SQLite 本地存储
- [ ] 聊天界面
- [ ] 文件传输

### 📋 待开发
- [ ] 语音视频通话
- [ ] 图片选择和发送
- [ ] 表情支持
- [ ] 推送通知
- [ ] 多语言支持

## 核心依赖

- **provider**: 状态管理
- **sqflite**: 本地数据库
- **image_picker**: 图片选择
- **file_picker**: 文件选择
- **shared_preferences**: 本地配置
- **permission_handler**: 权限管理

## 注意事项

1. **网络权限**: 
   - Android: 已在 AndroidManifest.xml 中配置
   - iOS: 需在 Info.plist 中添加网络权限说明

2. **存储权限**:
   - Android 11+ 需要特殊处理 (Scoped Storage)
   - iOS 通过 image_picker 自动处理

3. **局域网发现**:
   - 需要设备连接到同一 WiFi
   - 某些路由器可能阻止多播

## 测试

```bash
# 运行测试
flutter test

# 集成测试
flutter drive --target=test_driver/app.dart
```

## 调试

```bash
# 查看日志
flutter logs

# 分析代码
flutter analyze

# 格式化代码
dart format .
```

## 性能优化

- 使用 `const` 构造函数
- 避免不必要的 rebuild
- 图片压缩和缓存
- 消息列表虚拟化

## 常见问题

### Q: Flutter SDK 下载慢？
A: 使用国内镜像：
```bash
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
```

### Q: Android 编译失败？
A: 检查 minSdkVersion >= 21，清理缓存：
```bash
flutter clean
flutter pub get
```

### Q: iOS 编译失败？
A: 更新 CocoaPods：
```bash
cd ios
pod install --repo-update
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
