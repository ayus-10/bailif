import { API_URL } from "@/config";

/** @typedef {import('@/types/gantt').Gantt} Gantt */

/**
 * @param {string} projectId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Gantt>}
 */
export async function fetchGantt(projectId, signal) {
    const response = await fetch(`${API_URL}/gantt/${projectId}`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch gantt (${response.status})`);
    }

    /** @type {Gantt} */
    const data = await response.json();

    return data;
}
