import { defineStore } from "pinia";
import {
    addTaskToBoard,
    createTaskboard,
    deleteTaskboard,
    getTaskboard,
    listTaskboards,
    removeTaskFromBoard,
    repositionTask,
    updateTaskboard,
} from "@/api/taskboard.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

/** @typedef {import("@/types/taskboard").TaskboardRead} TaskboardRead */
/** @typedef {import("@/types/taskboard").TaskboardListRead} TaskboardListRead */
/** @typedef {import("@/types/taskboard").TaskboardCreate} TaskboardCreate */
/** @typedef {import("@/types/taskboard").TaskboardUpdate} TaskboardUpdate */
/** @typedef {import("@/types/taskboard").TaskAssignment} TaskAssignment */
/** @typedef {import("@/types/taskboard").TaskReposition} TaskReposition */
/** @typedef {import("@/types/taskboard").TaskboardTaskRead} TaskboardTaskRead */
/** @typedef {import("@/types/shared").FetchStatus} FetchStatus */

/**
 * @typedef {Object} TaskboardsState
 * @property {TaskboardListRead[]} items
 * @property {TaskboardRead | null} currentTaskboard
 * @property {FetchStatus} status
 * @property {any} error
 */

export const useTaskboardsStore = defineStore("taskboards", {
    /** @returns {TaskboardsState} */
    state: () => ({
        items: [],
        currentTaskboard: null,
        status: "idle",
        error: null,
    }),

    actions: {
        /**
         * @param {Object} [options]
         * @param {string} [options.projectId]
         * @param {boolean} [options.forceRefresh=false]
         */
        async fetch({ projectId, forceRefresh = false } = {}) {
            if (this.status === "loading" && !forceRefresh) return;
            this.status = "loading";
            this.error = null;

            const cacheKey = projectId
                ? `taskboards:project:${projectId}`
                : "taskboards:all";

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listTaskboards(projectId),
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
         * @param {string} boardId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<TaskboardRead | undefined>}
         */
        async get(boardId, { forceRefresh = false } = {}) {
            try {
                const board = await cachedRequest(
                    `taskboard:${boardId}`,
                    () => getTaskboard(boardId),
                    { forceRefresh }
                );
                this.currentTaskboard = board;
                return board;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {TaskboardCreate} payload
         * @returns {Promise<TaskboardRead | undefined>}
         */
        async create(payload) {
            try {
                const board = await createTaskboard(payload);
                this.items = [...this.items, { ...board, task_count: 0 }]; // TODO: figure out if this is safe

                invalidateRequestCache("taskboards:all");
                return board;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {TaskboardUpdate} payload
         * @returns {Promise<TaskboardRead | undefined>}
         */
        async update(boardId, payload) {
            try {
                const index = this.items.findIndex(
                    (item) => item.id === boardId
                );

                if (index === -1) return;

                const board = await updateTaskboard(boardId, payload);

                this.items = [
                    ...this.items.slice(0, index),
                    { ...board, task_count: this.items[index].task_count }, // TODO: figure out if this is safe
                    ...this.items.slice(index + 1),
                ];

                if (this.currentTaskboard?.id === boardId) {
                    this.currentTaskboard = board;
                }

                invalidateRequestCache(`taskboard:${boardId}`);
                invalidateRequestCache("taskboards:all");

                return board;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} boardId
         */
        async remove(boardId) {
            try {
                await deleteTaskboard(boardId);

                this.items = this.items.filter((item) => item.id !== boardId);

                if (this.currentTaskboard?.id === boardId) {
                    this.currentTaskboard = null;
                }

                invalidateRequestCache(`taskboard:${boardId}`);
                invalidateRequestCache("taskboards:all");
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {TaskAssignment} payload
         * @returns {Promise<TaskboardTaskRead | undefined>}
         */
        async addTask(boardId, payload) {
            try {
                const task = await addTaskToBoard(boardId, payload);

                if (this.currentTaskboard?.id === boardId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: [...(this.currentTaskboard.tasks ?? []), task],
                    };
                }

                invalidateRequestCache(`taskboard:${boardId}`);

                return task;
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         */
        async removeTask(boardId, taskId) {
            try {
                await removeTaskFromBoard(boardId, taskId);

                if (this.currentTaskboard?.id === boardId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: (this.currentTaskboard.tasks ?? []).filter(
                            (t) => t.id !== taskId
                        ),
                    };
                }

                invalidateRequestCache(`taskboard:${boardId}`);
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {TaskReposition} payload
         */
        async repositionTask(boardId, payload) {
            try {
                await repositionTask(boardId, payload);

                // TODO: this shit is borked

                // if (this.currentTaskboard?.id === boardId) {
                //     this.currentTaskboard = null;
                // }

                // invalidateRequestCache(`taskboard:${boardId}`);
            } catch (err) {
                this.error = err;
                this.status = "error";
            }
        },
    },
});
