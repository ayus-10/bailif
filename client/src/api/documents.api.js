import { API_URL } from "@/config";

/** @typedef {import('@/types/document').Document} Document */

/**
 * @param {string} scopeId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Document[]>}
 */
export async function fetchDocuments(scopeId, signal) {
    const response = await fetch(`${API_URL}/documents/${scopeId}`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch documents (${response.status})`);
    }

    /** @type {Document[]} */
    const data = await response.json();

    return data;
}
