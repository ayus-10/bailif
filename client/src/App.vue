<script setup>
import { ref, onMounted } from 'vue'
import { fetchTasks } from './services/api'
import TaskCard from './components/TaskCard.vue'
import AgentBar from './components/AgentBar.vue'

const tasks = ref([])
const loadingTasks = ref(true)
const loadError = ref('')

async function loadTasks() {
  loadingTasks.value = true
  loadError.value = ''
  try {
    tasks.value = await fetchTasks()
  } catch (err) {
    loadError.value = `Failed to load tasks: ${err.message}`
  } finally {
    loadingTasks.value = false
  }
}

onMounted(loadTasks)
</script>

<template>
  <div class="app">
    <header>
      <h1>Agentic Task Manager</h1>
    </header>

    <main>
      <AgentBar />

      <div class="task-list-header">
        <h2>Tasks</h2>
        <button class="refresh" @click="loadTasks">Refresh</button>
      </div>

      <p v-if="loadingTasks">Loading tasks...</p>
      <p v-else-if="loadError" class="error">{{ loadError }}</p>
      <p v-else-if="tasks.length === 0">No tasks yet.</p>
      <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
    </main>
  </div>
</template>

<style scoped>
.app {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px 16px;
}

header h1 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.task-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.refresh {
  border: 1px solid #ccc;
  background: white;
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 0.8rem;
  cursor: pointer;
}

.error {
  color: #c62828;
}
</style>
