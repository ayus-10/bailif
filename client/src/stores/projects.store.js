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
 * @typedef {import("@/types/project").ProjectsState} ProjectsState
 * @typedef {import("@/types/shared").RequestStatus} RequestStatus
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

/**
 * @param {string} operation
 * @param {number} projectPublicId
 * @returns {string}
 */
function mutationKey(operation, projectPublicId) {
    return [operation, projectPublicId].join(":");
}

export const useProjectsStore = defineStore("projects", {
    /**
     * @returns {ProjectsState}
     */
    state: () => ({
        items: [],
        currentProject: null,
        fetchStatus: {},
        fetchErrors: {},
        mutationStatus: {},
        mutationErrors: {},
    }),

    actions: {
        /**
         * @param {Object} [options]
         * @param {ProjectFilterParams} [options.params]
         * @param {boolean} [options.forceRefresh=false]
         * @throws {ApiError}
         */
        async fetch({ params = {}, forceRefresh = false } = {}) {
            const filterKey = createFilterKey(params);
            const key = `list:${filterKey}`;

            if (this.fetchStatus[key] === "loading" && !forceRefresh) {
                return;
            }

            this.fetchStatus[key] = "loading";
            this.fetchErrors[key] = null;

            const cacheKey = `projects:all${filterKey ? `:${filterKey}` : ""}`;

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listProjects(params),
                    { forceRefresh }
                );

                this.items = data.items;
                this.fetchStatus[key] = "success";

                return data;
            } catch (err) {
                this.fetchErrors[key] = err;
                this.fetchStatus[key] = "error";
                throw err;
            }
        },

        /**
         * @param {number} projectPublicId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<ProjectRead | undefined>}
         * @throws {ApiError}
         */
        async get(projectPublicId, { forceRefresh = false } = {}) {
            const key = `project:${projectPublicId}`;

            if (this.fetchStatus[key] === "loading" && !forceRefresh) {
                return;
            }

            this.fetchStatus[key] = "loading";
            this.fetchErrors[key] = null;

            try {
                const project = await cachedRequest(
                    key,
                    () => getProject(projectPublicId),
                    { forceRefresh }
                );

                this.currentProject = project;
                this.fetchStatus[key] = "success";

                return project;
            } catch (err) {
                this.fetchErrors[key] = err;
                this.fetchStatus[key] = "error";
                throw err;
            }
        },

        /**
         * @param {ProjectCreate} payload
         * @returns {Promise<ProjectRead>}
         * @throws {ApiError}
         */
        async create(payload) {
            const key = "create";

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                const project = await createProject(payload);

                this.items = [...this.items, project];

                invalidateRequestCache(`projects:all`);

                this.mutationStatus[key] = "success";

                return project;
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },

        /**
         * @param {number} projectPublicId
         * @param {ProjectUpdate} payload
         * @returns {Promise<ProjectRead>}
         * @throws {ApiError}
         */
        async update(projectPublicId, payload) {
            const key = mutationKey("update", projectPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

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

                this.mutationStatus[key] = "success";

                return project;
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },

        /**
         * @param {number} projectPublicId
         * @throws {ApiError}
         */
        async remove(projectPublicId) {
            const key = mutationKey("delete", projectPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

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

                this.mutationStatus[key] = "success";
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },
    },

    getters: {
        /**
         * @param {ProjectsState} state
         * @returns {(params?: ProjectFilterParams) => RequestStatus | null}
         */
        fetchStatusByFilter:
            (state) =>
            (params = {}) => {
                const key = `list:${createFilterKey(params)}`;

                return state.fetchStatus[key] ?? null;
            },

        /**
         * @param {ProjectsState} state
         * @returns {(params?: ProjectFilterParams) => unknown}
         */
        fetchErrorByFilter:
            (state) =>
            (params = {}) => {
                const key = `list:${createFilterKey(params)}`;

                return state.fetchErrors[key] ?? null;
            },

        /**
         * @param {ProjectsState} state
         * @returns {(projectPublicId: number) => RequestStatus | null}
         */
        fetchStatusByProject: (state) => (projectPublicId) => {
            return state.fetchStatus[`project:${projectPublicId}`] ?? null;
        },

        /**
         * @param {ProjectsState} state
         * @returns {(projectPublicId: number) => unknown}
         */
        fetchErrorByProject: (state) => (projectPublicId) => {
            return state.fetchErrors[`project:${projectPublicId}`] ?? null;
        },

        /**
         * @param {ProjectsState} state
         * @returns {(operation: string, id: number) => RequestStatus | null}
         */
        mutationStatusByKey: (state) => (operation, id) => {
            return state.mutationStatus[mutationKey(operation, id)] ?? null;
        },

        /**
         * @param {ProjectsState} state
         * @returns {(operation: string, id: number) => unknown}
         */
        mutationErrorByKey:
            (state) =>
            (operation, ...ids) => {
                return (
                    state.mutationErrors[mutationKey(operation, ...ids)] ?? null
                );
            },
    },
});
