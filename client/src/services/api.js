// Single choke point for all calls to the FastAPI backend.
// Swap the base URL via .env (see .env.example) without touching this file.

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchTasks() {
  const res = await fetch(`${BASE_URL}/tasks`)
  if (!res.ok) throw new Error(`Failed to load tasks: ${res.status}`)
  return res.json()
}

export async function createTask({ title, description = '', assignee = '', tags = '' }) {
  const res = await fetch(`${BASE_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, assignee, tags }),
  })
  if (!res.ok) throw new Error(`Failed to create task: ${res.status}`)
  return res.json()
}

/**
 * Streams the agent's response from /agent/query.
 * The backend sends SSE with `data: {...}\n\n` frames.
 * We use fetch + a manual reader instead of EventSource because
 * EventSource only supports GET — our endpoint needs POST with a body.
 *
 * @param {string} message - the user's natural language query
 * @param {(event: object) => void} onEvent - called for each parsed SSE event
 * @param {(err: Error) => void} onError
 */
export async function streamAgentQuery(message, onEvent, onError) {
  try {
    const res = await fetch(`${BASE_URL}/agent/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })

    if (!res.ok || !res.body) {
      throw new Error(`Agent request failed: ${res.status}`)
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })

      // SSE frames are separated by a blank line ("\n\n")
      const frames = buffer.split('\n\n')
      buffer = frames.pop() // keep any incomplete trailing frame for next chunk

      for (const frame of frames) {
        const line = frame.split('\n').find((l) => l.startsWith('data: '))
        if (!line) continue
        const jsonStr = line.slice('data: '.length)
        try {
          onEvent(JSON.parse(jsonStr))
        } catch {
          // Ignore malformed frames rather than killing the whole stream
        }
      }
    }
  } catch (err) {
    onError(err)
  }
}
