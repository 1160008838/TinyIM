/// 消息类型枚举
enum MessageType {
  text,
  image,
  file,
  voice,
  video,
  emoji,
  system,
}

/// 消息模型
class Message {
  final String msgId;
  final String senderId;
  final String receiverId;
  final MessageType msgType;
  final dynamic content;
  final DateTime timestamp;
  final bool isGroup;
  bool isRead;

  Message({
    required this.msgId,
    required this.senderId,
    required this.receiverId,
    required this.msgType,
    required this.content,
    required this.timestamp,
    this.isGroup = false,
    this.isRead = false,
  });

  Map<String, dynamic> toJson() {
    return {
      'msg_id': msgId,
      'sender_id': senderId,
      'receiver_id': receiverId,
      'msg_type': msgType.toString().split('.').last,
      'content': content,
      'timestamp': timestamp.toIso8601String(),
      'is_group': isGroup,
      'is_read': isRead,
    };
  }

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      msgId: json['msg_id'],
      senderId: json['sender_id'],
      receiverId: json['receiver_id'],
      msgType: MessageType.values.firstWhere(
        (e) => e.toString().split('.').last == json['msg_type'],
      ),
      content: json['content'],
      timestamp: DateTime.parse(json['timestamp']),
      isGroup: json['is_group'] ?? false,
      isRead: json['is_read'] ?? false,
    );
  }
}
