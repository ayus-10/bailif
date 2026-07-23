<script setup>
defineProps({
  task: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="task-card">
    <h3>{{ task.title }}</h3>
    <p v-if="task.description">{{ task.description }}</p>
    <div class="tags">
      <span v-if="task.assignee" class="chip">{{ task.assignee }}</span>
      <span class="chip status">{{ task.status }}</span>
    </div>
  </div>
</template>

<style scoped>
.task-card {
  background: white;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 10px;
  text-align: left;
}

.task-card h3 {
  margin: 0 0 4px;
  font-size: 1rem;
}

.task-card p {
  margin: 0 0 8px;
  font-size: 0.875rem;
  color: #555;
}

.tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.chip {
  background: #eef0ff;
  color: #3949ab;
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 0.75rem;
}

.chip.status {
  background: #e8f5e9;
  color: #2e7d32;
}
</style>
