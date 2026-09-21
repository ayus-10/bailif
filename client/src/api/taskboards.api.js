import { apiFetch } from "./client";
import { parseJson } from "./shared.api";

/**
 * @typedef {import("@/types/taskboards").TaskboardCreate} TaskboardCreate
 */
/**
 * @typedef {import("@/types/taskboards").TaskboardUpdate} TaskboardUpdate
 */
/**
 * @typedef {import("@/types/taskboards").TaskboardRead} TaskboardRead
 */
/**
 * @typedef {import("@/types/taskboards").TaskboardListRead} TaskboardListRead
 */
/**
 * @typedef {import("@/types/taskboards").TaskboardTaskRead} TaskboardTaskRead
 */
/**
 * @typedef {import("@/types/taskboards").TaskAssignment} TaskAssignment
 */
/**
 * @typedef {import("@/types/taskboards").TaskReposition} TaskReposition
 */
/**
 * @typedef {import("@/types/taskboards").TaskboardListResponse} TaskboardListResponse
 */

/**
 * @param {number} projectPublicId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskboardListResponse>}
 */
export async function listTaskboards(projectPublicId, signal) {
    const search = new URLSearchParams();

    search.set("project_public_id", String(projectPublicId));

    const response = await apiFetch(`/taskboards?${search}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @param {AbortSignal} [signal]
 * @returns {Promise<TaskboardRead>}
 */
export async function getTaskboard(publicId, signal) {
    const response = await apiFetch(`/taskboards/${publicId}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {TaskboardCreate} payload
 * @returns {Promise<TaskboardRead>}
 */
export async function createTaskboard(payload) {
    const response = await apiFetch(`/taskboards`, {
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
 * @param {TaskboardUpdate} payload
 * @returns {Promise<TaskboardRead>}
 */
export async function updateTaskboard(publicId, payload) {
    const response = await apiFetch(`/taskboards/${publicId}`, {
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
export async function deleteTaskboard(publicId) {
    const response = await apiFetch(`/taskboards/${publicId}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {number} boardPublicId
 * @param {TaskAssignment} payload
 * @returns {Promise<TaskboardTaskRead>}
 */
export async function addTaskToBoard(boardPublicId, payload) {
    const response = await apiFetch(`/taskboards/${boardPublicId}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {number} boardPublicId
 * @param {number} taskPublicId
 * @returns {Promise<void>}
 */
export async function removeTaskFromBoard(boardPublicId, taskPublicId) {
    const response = await apiFetch(
        `/taskboards/${boardPublicId}/tasks/${taskPublicId}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}

/**
 * @param {number} boardPublicId
 * @param {number} taskPublicId
 * @param {TaskReposition} payload
 * @returns {Promise<void>}
 */
export async function repositionTask(boardPublicId, taskPublicId, payload) {
    const response = await apiFetch(
        `/taskboards/${boardPublicId}/tasks/${taskPublicId}`,
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
