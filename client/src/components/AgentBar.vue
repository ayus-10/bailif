<script setup>
import { ref } from 'vue'
import { streamAgentQuery } from '../services/api'

const query = ref('')
const status = ref('')
const answer = ref('')
const loading = ref(false)

async function askAgent() {
  const message = query.value.trim()
  if (!message) return

  status.value = 'Thinking...'
  answer.value = ''
  loading.value = true

  await streamAgentQuery(
    message,
    (event) => {
      switch (event.stage) {
        case 'thinking':
          status.value = event.message || 'Thinking...'
          break
        case 'tool_call':
          status.value = `Using tool: ${event.tool}`
          break
        case 'tool_result':
          status.value = 'Got results, composing answer...'
          break
        case 'answer':
          status.value = ''
          answer.value = event.message || ''
          loading.value = false
          break
      }
    },
    (err) => {
      status.value = ''
      answer.value = `Agent error: ${err.message}`
      loading.value = false
    },
  )
}
</script>

<template>
  <div class="agent-bar">
    <div class="input-row">
      <input
        v-model="query"
        type="text"
        placeholder='Ask the agent: "overdue tasks for Sarah" or "anything about the login redesign?"'
        @keyup.enter="askAgent"
      />
      <button :disabled="loading" @click="askAgent">
        {{ loading ? '...' : 'Ask' }}
      </button>
    </div>
    <div v-if="status || answer" class="response">
      {{ answer || status }}
    </div>
  </div>
</template>

<style scoped>
.agent-bar {
  margin-bottom: 20px;
}

.input-row {
  display: flex;
  gap: 8px;
}

.input-row input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
}

.input-row button {
  padding: 10px 18px;
  border: none;
  border-radius: 6px;
  background: #3949ab;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.input-row button:disabled {
  opacity: 0.6;
  cursor: default;
}

.response {
  margin-top: 10px;
  padding: 12px;
  background: #f5f5f7;
  border-radius: 6px;
  font-size: 0.9rem;
  text-align: left;
}
</style>
