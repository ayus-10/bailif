import { apiFetch } from "./client";

/** @typedef {import("@/types/settings").Settings} Settings */

/**
 * @param {string} scopeId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Settings>}
 */
export async function fetchSettings(scopeId, signal) {
    const response = await apiFetch(`/settings/${scopeId}`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch settings (${response.status})`);
    }

    /** @type {Settings} */
    const data = await response.json();

    return data;
}
