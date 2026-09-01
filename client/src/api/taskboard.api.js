import { API_URL } from "@/config";
import { parseJson } from "./shared.api";

/** @typedef {import('@/types/taskboard').TaskboardCreate} TaskboardCreate */
/** @typedef {import('@/types/taskboard').TaskboardUpdate} TaskboardUpdate */
/** @typedef {import('@/types/taskboard').TaskboardRead} TaskboardRead */
/** @typedef {import('@/types/taskboard').TaskboardListRead} TaskboardListRead */
/** @typedef {import('@/types/taskboard').TaskboardTaskRead} TaskboardTaskRead */
/** @typedef {import('@/types/taskboard').TaskAssignment} TaskAssignment */
/** @typedef {import('@/types/taskboard').TaskReposition} TaskReposition */
/** @typedef {import('@/types/taskboard').TaskboardListResponse} TaskboardListResponse */

/**
 * @param {string} projectId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskboardListResponse>}
 */
export async function listTaskboards(projectId, signal) {
    const search = new URLSearchParams();

    search.set("project_id", projectId);

    const response = await fetch(`${API_URL}/taskboards?${search}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskboardRead>}
 */
export async function getTaskboard(id, signal) {
    const response = await fetch(`${API_URL}/taskboards/${id}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskboardCreate} payload
 * @returns {Promise<TaskboardRead>}
 */
export async function createTaskboard(payload) {
    const response = await fetch(`${API_URL}/taskboards`, {
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
 * @param {TaskboardUpdate} payload
 * @returns {Promise<TaskboardRead>}
 */
export async function updateTaskboard(id, payload) {
    const response = await fetch(`${API_URL}/taskboards/${id}`, {
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
export async function deleteTaskboard(id) {
    const response = await fetch(`${API_URL}/taskboards/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {string} boardId
 * @param {TaskAssignment} payload
 * @returns {Promise<TaskboardTaskRead>}
 */
export async function addTaskToBoard(boardId, payload) {
    const response = await fetch(`${API_URL}/taskboards/${boardId}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} boardId
 * @param {string} taskId
 * @returns {Promise<void>}
 */
export async function removeTaskFromBoard(boardId, taskId) {
    const response = await fetch(
        `${API_URL}/taskboards/${boardId}/tasks/${taskId}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {string} boardId
 * @param {TaskReposition} payload
 * @returns {Promise<void>}
 */
export async function repositionTask(boardId, payload) {
    const response = await fetch(
        `${API_URL}/taskboards/${boardId}/tasks/reposition`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        }
    );

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
