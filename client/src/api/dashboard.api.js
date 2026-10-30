import { apiFetch } from "./client";
import { parseJson } from "./shared.api";

/**
 * @typedef {import("@/types/dashboard").Dashboard} Dashboard
 */

/**
 * @param {AbortSignal} [signal]
 * @returns {Promise<Dashboard>}
 */
export async function fetchDashboard(signal) {
    const response = await apiFetch("/dashboard", { signal });

    return parseJson(response);
}
