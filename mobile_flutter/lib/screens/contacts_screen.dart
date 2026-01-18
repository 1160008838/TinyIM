import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_service.dart';

/// 联系人列表屏幕
class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('联系人'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              // TODO: 刷新设备列表
            },
          ),
        ],
      ),
      body: Consumer<AppService>(
        builder: (context, appService, child) {
          final devices = appService.devices;
          
          if (devices.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.devices, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('暂无在线设备', style: TextStyle(color: Colors.grey)),
                  SizedBox(height: 8),
                  Text('请确保设备连接到同一局域网', style: TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              ),
            );
          }
          
          return ListView.builder(
            itemCount: devices.length,
            itemBuilder: (context, index) {
              final device = devices[index];
              return ListTile(
                leading: CircleAvatar(
                  child: Text(device.nickname[0]),
                ),
                title: Text(device.nickname),
                subtitle: Text(device.ipAddress),
                trailing: device.isOnline
                    ? const Icon(Icons.circle, color: Colors.green, size: 12)
                    : const Icon(Icons.circle, color: Colors.grey, size: 12),
                onTap: () {
                  // TODO: 打开聊天界面
                },
              );
            },
          );
        },
      ),
    );
  }
}
