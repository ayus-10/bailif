import { API_URL } from "@/config";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskListResponse} TaskListResponse */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/task').TaskUpdate} TaskUpdate */
/** @typedef {import('@/types/task').TaskListParams} TaskListParams */
/** @typedef {import('@/types/task').TaskDependencyRead} TaskDependencyRead */
/** @typedef {import('@/types/task').TaskDependencyCreate} TaskDependencyCreate */

/**
 * @param {Response} response
 * @returns {Promise<any>}
 */
async function parseJson(response) {
    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }

    return response.json();
}

/**
 * @param {TaskListParams} [params]
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskListResponse>}
 */
export async function listTasks(params = {}, signal) {
    const search = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
        if (value != null) {
            search.set(key, String(value));
        }
    }

    const response = await fetch(`${API_URL}/tasks?${search.toString()}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskRead>}
 */
export async function getTask(id, signal) {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskCreate} payload
 * @returns {Promise<TaskRead>}
 */
export async function createTask(payload) {
    const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {TaskUpdate} payload
 * @returns {Promise<TaskRead>}
 */
export async function updateTask(id, payload) {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @returns {Promise<void>}
 */
export async function deleteTask(id) {
    const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {string} taskId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskDependencyRead[]>}
 */
export async function listDependencies(taskId, signal) {
    const response = await fetch(`${API_URL}/tasks/${taskId}/dependencies`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {string} taskId
 * @param {string} dependencyId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskDependencyRead>}
 */
export async function getDependency(taskId, dependencyId, signal) {
    const response = await fetch(
        `${API_URL}/tasks/${taskId}/dependencies/${dependencyId}`,
        { signal }
    );

    return parseJson(response);
}

/**
 * @param {string} taskId
 * @param {TaskDependencyCreate} payload
 * @returns {Promise<TaskDependencyRead>}
 */
export async function createDependency(taskId, payload) {
    const response = await fetch(`${API_URL}/tasks/${taskId}/dependencies`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} taskId
 * @param {string} dependencyId
 * @returns {Promise<void>}
 */
export async function deleteDependency(taskId, dependencyId) {
    const response = await fetch(
        `${API_URL}/tasks/${taskId}/dependencies/${dependencyId}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
