import 'package:flutter/material.dart';
import '../models/task.dart';

class TaskCard extends StatelessWidget {
  final Task task;

  const TaskCard({super.key, required this.task});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(task.title, style: Theme.of(context).textTheme.titleMedium),
            if (task.description.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(task.description, style: Theme.of(context).textTheme.bodySmall),
            ],
            const SizedBox(height: 8),
            Wrap(
              spacing: 6,
              children: [
                if (task.assignee.isNotEmpty) Chip(label: Text(task.assignee)),
                Chip(label: Text(task.status)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
