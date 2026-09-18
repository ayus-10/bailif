import { apiFetch } from "./client";
import { parseJson } from "./shared.api";

/** @typedef {import("@/types/ai-actions").ChatRequest} ChatRequest */
/** @typedef {import("@/types/ai-actions").ChatResponse} ChatResponse */
/** @typedef {import("@/types/ai-actions").ChatMode} ChatMode */
/** @typedef {import("@/types/ai-actions").AcceptActionResponse} AcceptActionResponse */

/**
 * @param {ChatRequest} payload
 * @param {AbortSignal} [signal]
 * @returns {Promise<ChatResponse>}
 */
export async function chat(payload, signal) {
    const response = await apiFetch(`/ai/chat`, {
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
    const response = await apiFetch(`/ai/chat?mode=suggest_tasks`, {
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
    const response = await apiFetch(`/ai/chat?mode=search_tasks`, {
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
 * @param {string} actionId
 * @param {AbortSignal} [signal]
 * @returns {Promise<AcceptActionResponse>}
 */
export async function acceptAction(actionId, signal) {
    const response = await apiFetch(`/ai/chat/actions/${actionId}/accept`, {
        method: "POST",
        signal,
    });

    return parseJson(response);
}
