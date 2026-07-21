class Task {
  final String id;
  final String title;
  final String description;
  final String assignee;
  final String status;
  final String tags;

  Task({
    required this.id,
    required this.title,
    required this.description,
    required this.assignee,
    required this.status,
    required this.tags,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String? ?? '',
      assignee: json['assignee'] as String? ?? '',
      status: json['status'] as String? ?? 'open',
      tags: json['tags'] as String? ?? '',
    );
  }
}
