/** @typedef {import('@/types/dashboard').Dashboard} Dashboard */

/**
 * @param {string} scopeId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Dashboard>}
 */
export async function fetchDashboard(scopeId, signal) {
    const response = await fetch(`/api/v1/dashboard/${scopeId}`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch dashboard (${response.status})`);
    }

    /** @type {Dashboard} */
    const data = await response.json();

    return data;
}
