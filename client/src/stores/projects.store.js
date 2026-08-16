import { defineStore } from "pinia";
import {
    createProject,
    deleteProject,
    getProject,
    listProjects,
    updateProject,
} from "@/api/projects.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

/** @typedef {import("@/types/project").ProjectRead} ProjectRead */
/** @typedef {import("@/types/project").ProjectCreate} ProjectCreate */
/** @typedef {import("@/types/project").ProjectUpdate} ProjectUpdate */
/** @typedef {import('@/types/shared').FetchStatus} FetchStatus */

/**
 * @typedef {Object} ProjectsState
 * @property {ProjectRead[]} items
 * @property {ProjectRead | null} currentProject
 * @property {FetchStatus} status
 * @property {any} error
 */

export const useProjectsStore = defineStore("projects", {
    /** @returns {ProjectsState} */
    state: () => ({
        items: [],
        currentProject: null,
        status: "idle",
        error: null,
    }),

    actions: {
        /**
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         */
        async fetch({ forceRefresh = false } = {}) {
            if (this.status === "loading" && !forceRefresh) return;
            this.status = "loading";
            this.error = null;

            const cacheKey = `projects:all`;

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listProjects(),
                    { forceRefresh: false }
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
         * @param {string} projectId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<ProjectRead | undefined>}
         */
        async get(projectId, { forceRefresh = false } = {}) {
            try {
                const project = await cachedRequest(
                    `project:${projectId}`,
                    () => getProject(projectId),
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
         */
        async create(payload) {
            try {
                const project = await createProject(payload);

                this.items = [...this.items, project];

                invalidateRequestCache(`projects:all`);

                return project;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} projectId
         * @param {ProjectUpdate} payload
         * @returns {Promise<ProjectRead | undefined>}
         */
        async update(projectId, payload) {
            try {
                const project = await updateProject(projectId, payload);

                const index = this.items.findIndex(
                    (item) => item.id === projectId
                );

                if (index !== -1) {
                    this.items = [
                        ...this.items.slice(0, index),
                        project,
                        ...this.items.slice(index + 1),
                    ];
                }

                if (this.currentProject?.id === projectId) {
                    this.currentProject = project;
                }

                invalidateRequestCache(`projects:all`);
                invalidateRequestCache(`project:${projectId}`);

                return project;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} projectId
         */
        async remove(projectId) {
            try {
                await deleteProject(projectId);

                this.items = this.items.filter((item) => item.id !== projectId);

                if (this.currentProject?.id === projectId) {
                    this.currentProject = null;
                }

                invalidateRequestCache(`projects:all`);
                invalidateRequestCache(`project:${projectId}`);
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },
    },
});
