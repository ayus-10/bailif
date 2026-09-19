import { apiFetch } from "./client";
import { parseJson } from "./shared.api";

/** @typedef {import("@/types/project").ProjectRead} ProjectRead */
/** @typedef {import("@/types/project").ProjectCreate} ProjectCreate */
/** @typedef {import("@/types/project").ProjectUpdate} ProjectUpdate */
/** @typedef {import("@/types/project").ProjectFilterParams} ProjectFilterParams */
/** @typedef {import("@/types/project").ProjectListResponse} ProjectListResponse */

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

    const response = await apiFetch(`/projects?${search}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @param {AbortSignal} [signal]
 * @returns {Promise<ProjectRead>}
 */
export async function getProject(publicId, signal) {
    const response = await apiFetch(`/projects/${publicId}`, {
        signal,
    });

    return parseJson(response);
}

/**
 * @param {ProjectCreate} payload
 * @returns {Promise<ProjectRead>}
 */
export async function createProject(payload) {
    const response = await apiFetch(`/projects`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @param {ProjectUpdate} payload
 * @returns {Promise<ProjectRead>}
 */
export async function updateProject(publicId, payload) {
    const response = await apiFetch(`/projects/${publicId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    return parseJson(response);
}

/**
 * @param {number} publicId
 * @returns {Promise<void>}
 */
export async function deleteProject(publicId) {
    const response = await apiFetch(`/projects/${publicId}`, {
        method: "DELETE",
    });

    if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
    }
}
