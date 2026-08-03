import { API_URL } from "@/config";

/** @typedef {import('@/types/notification').Notification} Notification */

/**
 * @param {string} scopeId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Notification[]>}
 */
export async function fetchNotifications(scopeId, signal) {
    const response = await fetch(`${API_URL}/notifications/${scopeId}`, {
        signal,
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch notifications (${response.status})`);
    }

    /** @type {Notification[]} */
    const data = await response.json();

    return data;
}
