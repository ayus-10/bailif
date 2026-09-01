import { API_URL } from "@/config";
import { parseJson } from "./shared.api";

/** @typedef {import('@/types/project').ProjectRead} ProjectRead */
/** @typedef {import('@/types/project').ProjectCreate} ProjectCreate */
/** @typedef {import('@/types/project').ProjectUpdate} ProjectUpdate */
/** @typedef {import('@/types/project').ProjectFilterParams} ProjectFilterParams */
/** @typedef {import('@/types/project').ProjectListResponse} ProjectListResponse */

/**
 * @param {ProjectFilterParams} [params]
 * @param {AbortSignal} [signal]
 * @returns {Promise<ProjectListResponse>}
 */
export async function listProjects(params = {}, signal) {
    const search = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
        if (value != null) {
            search.set(key, String(value));
        }
    }

    const response = await fetch(`${API_URL}/projects?${search}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {AbortSignal} [signal]
 * @returns {Promise<ProjectRead>}
 */
export async function getProject(id, signal) {
    const response = await fetch(`${API_URL}/projects/${id}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {ProjectCreate} payload
 * @returns {Promise<ProjectRead>}
 */
export async function createProject(payload) {
    const response = await fetch(`${API_URL}/projects`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @param {ProjectUpdate} payload
 * @returns {Promise<ProjectRead>}
 */
export async function updateProject(id, payload) {
    const response = await fetch(`${API_URL}/projects/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {string} id
 * @returns {Promise<void>}
 */
export async function deleteProject(id) {
    const response = await fetch(`${API_URL}/projects/${id}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
