/// 设备信息模型
class DeviceInfo {
  final String deviceId;
  String nickname;
  String ipAddress;
  String avatarPath;
  bool isOnline;
  DateTime? lastSeen;

  DeviceInfo({
    required this.deviceId,
    required this.nickname,
    required this.ipAddress,
    this.avatarPath = 'default_avatar.png',
    this.isOnline = false,
    this.lastSeen,
  });

  Map<String, dynamic> toJson() {
    return {
      'device_id': deviceId,
      'nickname': nickname,
      'ip_address': ipAddress,
      'avatar_path': avatarPath,
      'is_online': isOnline,
    };
  }

  factory DeviceInfo.fromJson(Map<String, dynamic> json) {
    return DeviceInfo(
      deviceId: json['device_id'],
      nickname: json['nickname'],
      ipAddress: json['ip_address'],
      avatarPath: json['avatar_path'] ?? 'default_avatar.png',
      isOnline: json['is_online'] ?? false,
    );
  }
}
