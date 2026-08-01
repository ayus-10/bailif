/** @typedef {import('@/types/task').Task} Task */

/**
 * @param {string} boardId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Task[]>}
 */
export async function fetchTasks(boardId, signal) {
    const response = await fetch(`/api/v1/boards/${boardId}/tasks`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch tasks (${response.status})`);
    }

    /** @type {Task[]} */
    const data = await response.json();

    return data;
}
