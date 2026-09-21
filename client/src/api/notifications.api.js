import { apiFetch } from "./client";

/**
 * @typedef {import("@/types/notification").Notification} Notification
 */

/**
 * @param {string} scopeId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Notification[]>}
 */
export async function fetchNotifications(scopeId, signal) {
    const response = await apiFetch(`/notifications/${scopeId}`, {
        signal,
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch notifications (${response.status})`);
    }

    /**
     * @type {Notification[]}
     */
    const data = await response.json();

    return data;
}
