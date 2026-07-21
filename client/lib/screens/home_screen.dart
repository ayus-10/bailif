import 'package:flutter/material.dart';

import '../models/task.dart';
import '../services/api_service.dart';
import '../widgets/task_card.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _api = ApiService();
  final TextEditingController _queryController = TextEditingController();

  List<Task> _tasks = [];
  String _agentStatus = '';
  String _agentAnswer = '';
  bool _loadingTasks = true;

  @override
  void initState() {
    super.initState();
    _loadTasks();
  }

  Future<void> _loadTasks() async {
    setState(() => _loadingTasks = true);
    try {
      final tasks = await _api.fetchTasks();
      setState(() => _tasks = tasks);
    } catch (e) {
      setState(() => _agentAnswer = 'Failed to load tasks: $e');
    } finally {
      setState(() => _loadingTasks = false);
    }
  }

  void _askAgent() {
    final message = _queryController.text.trim();
    if (message.isEmpty) return;

    setState(() {
      _agentStatus = 'Thinking...';
      _agentAnswer = '';
    });

    _api.streamAgentQuery(
      message: message,
      onEvent: (event) {
        setState(() {
          switch (event['stage']) {
            case 'thinking':
              _agentStatus = event['message'] ?? 'Thinking...';
              break;
            case 'tool_call':
              _agentStatus = 'Using tool: ${event['tool']}';
              break;
            case 'tool_result':
              _agentStatus = 'Got results, composing answer...';
              break;
            case 'answer':
              _agentStatus = '';
              _agentAnswer = event['message'] ?? '';
              break;
          }
        });
      },
      onError: (e) {
        setState(() {
          _agentStatus = '';
          _agentAnswer = 'Agent error: $e';
        });
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Agentic Task Manager')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- Agent query bar ---
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _queryController,
                    decoration: const InputDecoration(
                      hintText: 'Ask the agent: "overdue tasks for Sarah" or "anything about the login redesign?"',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _askAgent(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(onPressed: _askAgent, child: const Text('Ask')),
              ],
            ),
            if (_agentStatus.isNotEmpty || _agentAnswer.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Card(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Text(_agentAnswer.isNotEmpty ? _agentAnswer : _agentStatus),
                  ),
                ),
              ),
            const SizedBox(height: 16),
            const Divider(),
            // --- Task board ---
            Expanded(
              child: _loadingTasks
                  ? const Center(child: CircularProgressIndicator())
                  : RefreshIndicator(
                      onRefresh: _loadTasks,
                      child: ListView.builder(
                        itemCount: _tasks.length,
                        itemBuilder: (context, i) => TaskCard(task: _tasks[i]),
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
