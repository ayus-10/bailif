import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const AgenticTaskApp());
}

class AgenticTaskApp extends StatelessWidget {
  const AgenticTaskApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Agentic Task Manager',
      theme: ThemeData(colorSchemeSeed: Colors.indigo, useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}
