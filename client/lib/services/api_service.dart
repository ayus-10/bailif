import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_client_sse/flutter_client_sse.dart';

import '../models/task.dart';

class ApiService {
  // Point this at your FastAPI server. Use --dart-define to swap between
  // local dev and a deployed backend without editing code:
  //   flutter run --dart-define=API_BASE_URL=http://localhost:8000
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  Future<List<Task>> fetchTasks() async {
    final res = await http.get(Uri.parse('$baseUrl/tasks'));
    if (res.statusCode != 200) {
      throw Exception('Failed to load tasks: ${res.statusCode}');
    }
    final List<dynamic> data = jsonDecode(res.body);
    return data.map((e) => Task.fromJson(e)).toList();
  }

  Future<Task> createTask({
    required String title,
    String description = '',
    String assignee = '',
    String tags = '',
  }) async {
    final res = await http.post(
      Uri.parse('$baseUrl/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'title': title,
        'description': description,
        'assignee': assignee,
        'tags': tags,
      }),
    );
    if (res.statusCode != 200) {
      throw Exception('Failed to create task: ${res.statusCode}');
    }
    return Task.fromJson(jsonDecode(res.body));
  }

  /// Streams agent responses (thinking / tool_call / tool_result / answer)
  /// from the /agent/query SSE endpoint. `onEvent` fires for each stage.
  void streamAgentQuery({
    required String message,
    required void Function(Map<String, dynamic> event) onEvent,
    required void Function(Object error) onError,
  }) {
    SSEClient.subscribeToSSE(
      method: SSERequestType.POST,
      url: '$baseUrl/agent/query',
      header: {'Content-Type': 'application/json'},
      body: {'message': message},
    ).listen(
      (event) {
        if (event.data != null) {
          onEvent(jsonDecode(event.data!) as Map<String, dynamic>);
        }
      },
      onError: onError,
    );
  }
}
