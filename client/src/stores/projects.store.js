import { defineStore } from "pinia";
import {
    createProject,
    deleteProject,
    getProject,
    listProjects,
    updateProject,
} from "@/api/projects.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

/**
 * @typedef {import("@/api/shared.api").ApiError} ApiError
 * @typedef {import("@/types/project").ProjectRead} ProjectRead
 * @typedef {import("@/types/project").ProjectCreate} ProjectCreate
 * @typedef {import("@/types/project").ProjectUpdate} ProjectUpdate
 * @typedef {import("@/types/project").ProjectFilterParams} ProjectFilterParams
 * @typedef {import("@/types/shared").FetchStatus} FetchStatus
 */

/**
 * @typedef {Object} ProjectsState
 * @property {ProjectRead[]} items
 * @property {ProjectRead | null} currentProject
 * @property {FetchStatus} status
 * @property {any} error
 */

/**
 * @param {ProjectFilterParams} params
 * @returns {string}
 */
function createFilterKey(params = {}) {
    const {
        status = null,
        agent_enabled = null,
        start_date_before = null,
        start_date_after = null,
        target_end_date_before = null,
        target_end_date_after = null,
    } = params;

    return [
        status ?? "all",
        agent_enabled ?? "all",
        start_date_before ?? "none",
        start_date_after ?? "none",
        target_end_date_before ?? "none",
        target_end_date_after ?? "none",
    ].join(":");
}

export const useProjectsStore = defineStore("projects", {
    /**
     * @returns {ProjectsState}
     */
    state: () => ({
        items: [],
        currentProject: null,
        status: "idle",
        error: null,
    }),

    actions: {
        /**
         * @param {Object} [options]
         * @param {ProjectFilterParams} [options.params]
         * @param {boolean} [options.forceRefresh=false]
         */
        async fetch({ params = {}, forceRefresh = false } = {}) {
            if (this.status === "loading" && !forceRefresh) return;

            this.status = "loading";
            this.error = null;

            const filterKey = createFilterKey(params);

            const cacheKey = `projects:all${filterKey ? `:${filterKey}` : ""}`;

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listProjects(params),
                    { forceRefresh }
                );

                this.items = data.items;
                this.status = "success";

                return data;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {number} projectPublicId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<ProjectRead | undefined>}
         */
        async get(projectPublicId, { forceRefresh = false } = {}) {
            try {
                const project = await cachedRequest(
                    `project:${projectPublicId}`,
                    () => getProject(projectPublicId),
                    { forceRefresh }
                );

                this.currentProject = project;

                return project;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {ProjectCreate} payload
         * @returns {Promise<ProjectRead | undefined>}
         * @throws {ApiError}
         */
        async create(payload) {
            try {
                const project = await createProject(payload);

                this.items = [...this.items, project];

                invalidateRequestCache(`projects:all`);

                return project;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} projectPublicId
         * @param {ProjectUpdate} payload
         * @returns {Promise<ProjectRead | undefined>}
         * @throws {ApiError}
         */
        async update(projectPublicId, payload) {
            try {
                const project = await updateProject(projectPublicId, payload);

                const index = this.items.findIndex(
                    (item) => item.public_id === projectPublicId
                );

                if (index !== -1) {
                    this.items = [
                        ...this.items.slice(0, index),
                        project,
                        ...this.items.slice(index + 1),
                    ];
                }

                if (this.currentProject?.public_id === projectPublicId) {
                    this.currentProject = project;
                }

                invalidateRequestCache(`projects:all`);
                invalidateRequestCache(`project:${projectPublicId}`);

                return project;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} projectPublicId
         * @throws {ApiError}
         */
        async remove(projectPublicId) {
            try {
                await deleteProject(projectPublicId);

                this.items = this.items.filter(
                    (item) => item.public_id !== projectPublicId
                );

                if (this.currentProject?.public_id === projectPublicId) {
                    this.currentProject = null;
                }

                invalidateRequestCache(`projects:all`);
                invalidateRequestCache(`project:${projectPublicId}`);
            } catch (err) {
                throw err;
            }
        },
    },
});
