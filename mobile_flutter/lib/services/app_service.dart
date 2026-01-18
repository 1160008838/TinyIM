import 'package:flutter/material.dart';
import '../models/device_info.dart';
import '../models/message.dart';

/// 应用主服务类
/// 负责设备发现、消息收发、状态管理
class AppService extends ChangeNotifier {
  // 本地设备信息
  late DeviceInfo localDevice;
  
  // 在线设备列表
  final List<DeviceInfo> _devices = [];
  List<DeviceInfo> get devices => _devices;
  
  // 消息列表
  final Map<String, List<Message>> _messages = {};
  
  AppService() {
    _initialize();
  }
  
  void _initialize() {
    // 初始化本地设备
    localDevice = DeviceInfo(
      deviceId: _generateDeviceId(),
      nickname: _generateDefaultNickname(),
      ipAddress: '0.0.0.0', // 需要实际获取
    );
    
    // TODO: 启动设备发现服务
    // TODO: 启动TCP服务器
  }
  
  /// 生成设备ID
  String _generateDeviceId() {
    // TODO: 实现基于硬件信息的ID生成
    return 'DEVICE${DateTime.now().millisecondsSinceEpoch}';
  }
  
  /// 生成默认昵称
  String _generateDefaultNickname() {
    return 'Device-${DateTime.now().millisecondsSinceEpoch % 10000}';
  }
  
  /// 添加设备
  void addDevice(DeviceInfo device) {
    final index = _devices.indexWhere((d) => d.deviceId == device.deviceId);
    if (index >= 0) {
      _devices[index] = device;
    } else {
      _devices.add(device);
    }
    notifyListeners();
  }
  
  /// 移除设备
  void removeDevice(String deviceId) {
    _devices.removeWhere((d) => d.deviceId == deviceId);
    notifyListeners();
  }
  
  /// 发送消息
  Future<bool> sendMessage(Message message) async {
    // TODO: 实现TCP消息发送
    
    // 保存到本地
    final key = message.receiverId;
    if (!_messages.containsKey(key)) {
      _messages[key] = [];
    }
    _messages[key]!.add(message);
    notifyListeners();
    
    return true;
  }
  
  /// 获取聊天历史
  List<Message> getChatHistory(String peerId) {
    return _messages[peerId] ?? [];
  }
  
  /// 更新个人资料
  void updateProfile({String? nickname, String? avatarPath}) {
    if (nickname != null) {
      localDevice.nickname = nickname;
    }
    if (avatarPath != null) {
      localDevice.avatarPath = avatarPath;
    }
    notifyListeners();
  }
}
