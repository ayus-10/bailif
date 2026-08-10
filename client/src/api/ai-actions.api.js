import { API_URL } from "@/config";

/** @typedef {import('@/types/ai-actions').ChatRequest} ChatRequest */
/** @typedef {import('@/types/ai-actions').ChatResponse} ChatResponse */
/** @typedef {import('@/types/ai-actions').ChatMode} ChatMode */

/**
 * @param {Response} response
 * @returns {Promise<any>}
 */
async function parseJson(response) {
    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }

    return response.json();
}

/**
 * @param {ChatRequest} payload
 * @param {AbortSignal} [signal]
 * @returns {Promise<ChatResponse>}
 */
export async function chat(payload, signal) {
    const response = await fetch(`${API_URL}/ai/chat`, {
        method: "POST",
        signal,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {ChatRequest} payload
 * @param {AbortSignal} [signal]
 * @returns {Promise<ChatResponse>}
 */
export async function suggestTasks(payload, signal) {
    const response = await fetch(`${API_URL}/ai/chat?mode=suggest_tasks`, {
        method: "POST",
        signal,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {ChatRequest} payload
 * @param {AbortSignal} [signal]
 * @returns {Promise<ChatResponse>}
 */
export async function searchTasks(payload, signal) {
    const response = await fetch(`${API_URL}/ai/chat?mode=search_tasks`, {
        method: "POST",
        signal,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}
