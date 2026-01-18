# TinyIM 编译打包指南

## 1. 桌面端编译 (Python + PyQt6)

### 1.1 环境准备

#### Windows 10/11

```bash
# 1. 安装 Python 3.9 或更高版本
# 从 https://www.python.org/downloads/ 下载安装

# 2. 验证安装
python --version
pip --version

# 3. 安装依赖
cd desktop
pip install -r requirements.txt

# 4. 安装打包工具
pip install pyinstaller
```

#### Linux (Ubuntu 18.04+)

```bash
# 1. 安装 Python 3
sudo apt update
sudo apt install python3 python3-pip

# 2. 安装依赖
cd desktop
pip3 install -r requirements.txt

# 3. 安装打包工具
pip3 install pyinstaller
```

### 1.2 运行测试

```bash
# 进入桌面端目录
cd desktop

# 运行命令行版本
python main.py

# 测试基本功能
# 1. 查看在线设备: list
# 2. 发送消息: send <device_id> <message>
# 3. 查看历史: history <device_id>
```

### 1.3 打包为可执行文件

#### Windows EXE 打包

```bash
cd desktop

# 单文件打包 (推荐)
pyinstaller --onefile --windowed --name TinyIM main.py

# 包含资源文件
pyinstaller --onefile --windowed \
    --name TinyIM \
    --add-data "resources;resources" \
    main.py

# 输出文件位于: dist/TinyIM.exe
```

#### Linux 可执行文件打包

```bash
cd desktop

# 打包
pyinstaller --onefile --name TinyIM main.py

# 输出文件位于: dist/TinyIM
# 添加执行权限
chmod +x dist/TinyIM
```

### 1.4 创建安装包

#### Windows Installer (可选)

使用 **Inno Setup** 创建安装程序:

1. 下载安装 Inno Setup: https://jrsoftware.org/isinfo.php

2. 创建 `installer.iss` 脚本:

```ini
[Setup]
AppName=TinyIM
AppVersion=1.0
DefaultDirName={pf}\TinyIM
DefaultGroupName=TinyIM
OutputDir=output
OutputBaseFilename=TinyIM-Setup

[Files]
Source: "dist\TinyIM.exe"; DestDir: "{app}"
Source: "resources\*"; DestDir: "{app}\resources"

[Icons]
Name: "{group}\TinyIM"; Filename: "{app}\TinyIM.exe"
Name: "{commondesktop}\TinyIM"; Filename: "{app}\TinyIM.exe"
```

3. 编译安装包

---

## 2. 移动端编译 (Flutter)

### 2.1 环境准备

#### 安装 Flutter SDK

**Windows:**

```bash
# 1. 下载 Flutter SDK
# https://docs.flutter.dev/get-started/install/windows

# 2. 解压到 C:\flutter

# 3. 添加到环境变量 PATH
C:\flutter\bin

# 4. 运行 flutter doctor
flutter doctor
```

**macOS (for iOS development):**

```bash
# 1. 使用 Homebrew 安装
brew install flutter

# 2. 安装 Xcode
# 从 App Store 安装

# 3. 安装 CocoaPods
sudo gem install cocoapods

# 4. 运行 flutter doctor
flutter doctor
```

**Linux:**

```bash
# 1. 下载并解压 Flutter
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.x.x-stable.tar.xz
tar xf flutter_linux_3.x.x-stable.tar.xz

# 2. 添加到 PATH
export PATH="$PATH:`pwd`/flutter/bin"

# 3. 运行 flutter doctor
flutter doctor
```

### 2.2 创建 Flutter 项目

```bash
# 创建新项目
cd mobile_flutter
flutter create . --org com.tinyim --project-name tinyim

# 添加依赖
flutter pub add http sqflite path_provider shared_preferences
flutter pub add image_picker file_picker flutter_sound
flutter pub add provider get_it
```

### 2.3 Android 编译

#### 2.3.1 环境配置

```bash
# 1. 安装 Android Studio
# https://developer.android.com/studio

# 2. 安装 Android SDK (API 26+)
# 通过 Android Studio SDK Manager 安装

# 3. 配置环境变量
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

#### 2.3.2 配置签名 (Release)

创建 `android/key.properties`:

```properties
storePassword=<your-password>
keyPassword=<your-password>
keyAlias=tinyim
storeFile=<path-to-keystore>
```

生成密钥库:

```bash
keytool -genkey -v -keystore tinyim.jks -keyalg RSA -keysize 2048 -validity 10000 -alias tinyim
```

修改 `android/app/build.gradle`:

```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

#### 2.3.3 编译 APK

```bash
cd mobile_flutter

# Debug 版本
flutter build apk --debug

# Release 版本
flutter build apk --release

# Split APK (按架构分离，减小体积)
flutter build apk --split-per-abi

# 输出文件: build/app/outputs/flutter-apk/app-release.apk
```

#### 2.3.4 安装测试

```bash
# 连接 Android 设备或启动模拟器

# 查看设备
flutter devices

# 安装 APK
flutter install

# 或使用 adb
adb install build/app/outputs/flutter-apk/app-release.apk
```

### 2.4 iOS 编译 (需要 macOS)

#### 2.4.1 环境配置

```bash
# 1. 安装 Xcode (从 App Store)

# 2. 安装 Xcode Command Line Tools
xcode-select --install

# 3. 安装 CocoaPods
sudo gem install cocoapods

# 4. 安装依赖
cd mobile_flutter/ios
pod install
```

#### 2.4.2 配置签名

1. 在 Xcode 中打开 `ios/Runner.xcworkspace`
2. 选择 Runner -> Signing & Capabilities
3. 选择你的 Apple Developer Team
4. 设置 Bundle Identifier: `com.tinyim.app`

#### 2.4.3 编译 IPA

```bash
cd mobile_flutter

# 编译 iOS 应用
flutter build ios --release

# 创建 IPA (需要通过 Xcode)
# 1. 在 Xcode 中选择 Product -> Archive
# 2. 选择 Export -> Ad Hoc (测试) 或 App Store (发布)
```

---

## 3. 依赖库版本说明

### 3.1 Python 依赖 (desktop/requirements.txt)

```
PyQt6==6.6.1          # GUI框架
netifaces==0.11.0     # 网络接口信息
Pillow==10.2.0        # 图片处理
python-dotenv==1.0.0  # 环境变量
```

### 3.2 Flutter 依赖 (mobile_flutter/pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # 网络
  http: ^1.1.0
  
  # 数据库
  sqflite: ^2.3.0
  
  # 文件系统
  path_provider: ^2.1.1
  file_picker: ^6.1.1
  
  # 图片
  image_picker: ^1.0.4
  
  # 存储
  shared_preferences: ^2.2.2
  
  # 状态管理
  provider: ^6.1.1
  get_it: ^7.6.4
  
  # 音频
  flutter_sound: ^9.2.13
```

---

## 4. 构建脚本

### 4.1 Windows 批处理脚本

创建 `build.bat`:

```batch
@echo off
echo Building TinyIM for Windows...

cd desktop
pip install -r requirements.txt
pyinstaller --onefile --windowed --name TinyIM main.py

echo Build complete! Executable at: desktop\dist\TinyIM.exe
pause
```

### 4.2 Linux Shell 脚本

创建 `build.sh`:

```bash
#!/bin/bash
echo "Building TinyIM for Linux..."

cd desktop
pip3 install -r requirements.txt
pyinstaller --onefile --name TinyIM main.py

echo "Build complete! Executable at: desktop/dist/TinyIM"
chmod +x dist/TinyIM
```

### 4.3 移动端构建脚本

创建 `build_mobile.sh`:

```bash
#!/bin/bash

echo "Building TinyIM Mobile..."

cd mobile_flutter

# Android
echo "Building Android APK..."
flutter build apk --release --split-per-abi

# iOS (仅在 macOS 上)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Building iOS..."
    flutter build ios --release
fi

echo "Build complete!"
echo "Android APK: mobile_flutter/build/app/outputs/flutter-apk/"
```

---

## 5. 常见问题

### 5.1 Python 打包问题

**问题**: ModuleNotFoundError

**解决**: 确保所有依赖已安装
```bash
pip install -r requirements.txt --force-reinstall
```

**问题**: PyInstaller 打包后运行出错

**解决**: 使用 `--debug all` 参数查看详细错误
```bash
pyinstaller --onefile --debug all main.py
```

### 5.2 Flutter 编译问题

**问题**: Gradle 下载慢

**解决**: 配置国内镜像
```gradle
// android/build.gradle
repositories {
    maven { url 'https://maven.aliyun.com/repository/google' }
    maven { url 'https://maven.aliyun.com/repository/jcenter' }
    maven { url 'https://maven.aliyun.com/repository/public' }
}
```

**问题**: iOS 证书问题

**解决**: 使用 Xcode 自动管理签名，或手动配置 Provisioning Profile

### 5.3 网络权限问题

**Android**: 在 `android/app/src/main/AndroidManifest.xml` 添加:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
```

**iOS**: 在 `ios/Runner/Info.plist` 添加:

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>TinyIM需要访问本地网络以发现设备</string>
```

---

## 6. 发布检查清单

- [ ] 所有功能测试通过
- [ ] 无已知崩溃bug
- [ ] 版本号更新
- [ ] 图标和资源文件完整
- [ ] 用户协议和隐私政策
- [ ] 签名配置正确
- [ ] 测试多个设备互通
- [ ] 文档更新完整

---

## 7. 版本发布

### 版本号规则

采用语义化版本: `主版本.次版本.修订版本`

例如: `1.0.0`

- 主版本: 不兼容的API修改
- 次版本: 向下兼容的功能新增
- 修订版本: 向下兼容的问题修正

### 发布流程

1. 更新版本号
2. 编译所有平台版本
3. 测试安装包
4. 创建 Release Notes
5. 上传到发布渠道
