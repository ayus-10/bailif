/** @typedef {import('@/types/project').Project} Project */

/**
 * @param {string} projectId
 * @param {AbortSignal} [signal]
 * @returns {Promise<Project>}
 */
export async function fetchProject(projectId, signal) {
    const response = await fetch(`/api/v1/projects/${projectId}`, { signal });

    if (!response.ok) {
        throw new Error(`Failed to fetch project (${response.status})`);
    }

    /** @type {Project} */
    const data = await response.json();

    return data;
}
