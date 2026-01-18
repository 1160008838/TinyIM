import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'services/app_service.dart';

void main() {
  runApp(const TinyIMApp());
}

class TinyIMApp extends StatelessWidget {
  const TinyIMApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppService()),
      ],
      child: MaterialApp(
        title: 'TinyIM',
        theme: ThemeData(
          primarySwatch: Colors.green,
          useMaterial3: true,
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
