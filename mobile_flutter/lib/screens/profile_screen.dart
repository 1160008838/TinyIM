import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/app_service.dart';

/// 个人资料屏幕
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('我的'),
      ),
      body: Consumer<AppService>(
        builder: (context, appService, child) {
          final device = appService.localDevice;
          
          return ListView(
            children: [
              const SizedBox(height: 20),
              // 头像和昵称
              Center(
                child: Column(
                  children: [
                    CircleAvatar(
                      radius: 50,
                      child: Text(
                        device.nickname[0],
                        style: const TextStyle(fontSize: 32),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      device.nickname,
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      device.deviceId.substring(0, 8),
                      style: const TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 30),
              const Divider(),
              
              // 设置选项
              ListTile(
                leading: const Icon(Icons.edit),
                title: const Text('修改昵称'),
                onTap: () {
                  // TODO: 修改昵称
                },
              ),
              ListTile(
                leading: const Icon(Icons.photo),
                title: const Text('修改头像'),
                onTap: () {
                  // TODO: 修改头像
                },
              ),
              const Divider(),
              ListTile(
                leading: const Icon(Icons.settings),
                title: const Text('设置'),
                onTap: () {
                  // TODO: 打开设置
                },
              ),
              ListTile(
                leading: const Icon(Icons.info),
                title: const Text('关于'),
                trailing: const Text('v1.0.0', style: TextStyle(color: Colors.grey)),
                onTap: () {
                  _showAboutDialog(context);
                },
              ),
            ],
          );
        },
      ),
    );
  }
  
  void _showAboutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('关于 TinyIM'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('版本: 1.0.0'),
            SizedBox(height: 8),
            Text('TinyIM 是一款无服务器、局域网点对点的即时通讯软件'),
            SizedBox(height: 8),
            Text('© 2024 TinyIM'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('确定'),
          ),
        ],
      ),
    );
  }
}
