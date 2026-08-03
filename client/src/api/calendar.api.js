import { API_URL } from "@/config";

/** @typedef {import('@/types/calendar').Calendar} Calendar */

/**
 * @param {string} monthKey
 * @param {AbortSignal} [signal]
 * @returns {Promise<Calendar>}
 */
export async function fetchCalendar(monthKey, signal) {
    const response = await fetch(`${API_URL}/calendar/${monthKey}`, { signal });
    if (!response.ok) {
        throw new Error(`Failed to fetch calendar (${response.status})`);
    }
    /** @type {Calendar} */
    const data = await response.json();
    return data;
}
