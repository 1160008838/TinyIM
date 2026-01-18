import 'package:flutter/material.dart';

/// 视频会议屏幕
class MeetingsScreen extends StatelessWidget {
  const MeetingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('视频会议'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.video_call, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            const Text('暂无会议', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                // TODO: 创建会议
              },
              icon: const Icon(Icons.add),
              label: const Text('创建会议'),
            ),
          ],
        ),
      ),
    );
  }
}
