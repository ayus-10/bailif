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

    const response = await fetch(`/api/v1/tasks?${search.toString()}`, {
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
    const response = await fetch(`/api/v1/tasks/${id}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskCreate} payload
 * @returns {Promise<TaskRead>}
 */
export async function createTask(payload) {
    const response = await fetch("/api/v1/tasks", {
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
    const response = await fetch(`/api/v1/tasks/${id}`, {
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
    const response = await fetch(`/api/v1/tasks/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskDependencyRead[]>}
 */
export async function listDependencies(signal) {
    const response = await fetch("/api/v1/task-dependencies", {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskDependencyRead>}
 */
export async function getDependency(id, signal) {
    const response = await fetch(`/api/v1/task-dependencies/${id}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskDependencyCreate} payload
 * @returns {Promise<TaskDependencyRead>}
 */
export async function createDependency(payload) {
    const response = await fetch("/api/v1/task-dependencies", {
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
 * @returns {Promise<void>}
 */
export async function deleteDependency(id) {
    const response = await fetch(`/api/v1/task-dependencies/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
