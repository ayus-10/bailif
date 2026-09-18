import { apiFetch } from "./client";
import { parseJson } from "./shared.api";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskListResponse} TaskListResponse */
/** @typedef {import("@/types/task").TaskCreate} TaskCreate */
/** @typedef {import("@/types/task").TaskUpdate} TaskUpdate */
/** @typedef {import("@/types/task").TaskListParams} TaskListParams */

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

    const response = await apiFetch(`/tasks?${search.toString()}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskRead>}
 */
export async function getTask(publicId, signal) {
    const response = await apiFetch(`/tasks/${publicId}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskCreate} payload
 * @returns {Promise<TaskRead>}
 */
export async function createTask(payload) {
    const response = await apiFetch(`/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @param {TaskUpdate} payload
 * @returns {Promise<TaskRead>}
 */
export async function updateTask(publicId, payload) {
    const response = await apiFetch(`/tasks/${publicId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @returns {Promise<void>}
 */
export async function deleteTask(publicId) {
    const response = await apiFetch(`/tasks/${publicId}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
