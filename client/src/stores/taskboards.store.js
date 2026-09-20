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
} from "@/api/taskboards.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

/** @typedef {import("@/api/shared.api").ApiError} ApiError */
/** @typedef {import("@/types/taskboards").TaskboardRead} TaskboardRead */
/** @typedef {import("@/types/taskboards").TaskboardListRead} TaskboardListRead */
/** @typedef {import("@/types/taskboards").TaskboardCreate} TaskboardCreate */
/** @typedef {import("@/types/taskboards").TaskboardUpdate} TaskboardUpdate */
/** @typedef {import("@/types/taskboards").TaskAssignment} TaskAssignment */
/** @typedef {import("@/types/taskboards").TaskReposition} TaskReposition */
/** @typedef {import("@/types/taskboards").TaskboardTaskRead} TaskboardTaskRead */
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
         * @param {Object} options
         * @param {number} options.projectPublicId
         * @param {boolean} [options.forceRefresh=false]
         */
        async fetch({ projectPublicId, forceRefresh = false }) {
            if (this.status === "loading" && !forceRefresh) return;

            this.status = "loading";
            this.error = null;

            const cacheKey = `taskboards:project:${projectPublicId}`;

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listTaskboards(projectPublicId),
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
         * @param {number} boardPublicId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<TaskboardRead | undefined>}
         */
        async get(boardPublicId, { forceRefresh = false } = {}) {
            try {
                const board = await cachedRequest(
                    `taskboard:${boardPublicId}`,
                    () => getTaskboard(boardPublicId),
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
         * @throws {ApiError}
         */
        async create(payload) {
            try {
                const board = await createTaskboard(payload);

                this.items = [...this.items, { ...board, task_count: 0 }]; // TODO: figure out if this is safe

                invalidateRequestCache(
                    `taskboards:project:${board.project_public_id}`
                );

                return board;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {TaskboardUpdate} payload
         * @returns {Promise<TaskboardRead | undefined>}
         * @throws {ApiError}
         */
        async update(boardPublicId, payload) {
            try {
                const index = this.items.findIndex(
                    (item) => item.public_id === boardPublicId
                );

                if (index === -1) return;

                const board = await updateTaskboard(boardPublicId, payload);

                this.items = [
                    ...this.items.slice(0, index),
                    {
                        ...board,
                        task_count: this.items[index].task_count,
                    }, // TODO: figure out if this is safe
                    ...this.items.slice(index + 1),
                ];

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = board;
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);
                invalidateRequestCache(
                    `taskboards:project:${board.project_public_id}`
                );

                return board;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @throws {ApiError}
         */
        async remove(boardPublicId) {
            try {
                const board = this.items.find(
                    (item) => item.public_id === boardPublicId
                );
                if (!board) return;

                await deleteTaskboard(boardPublicId);

                this.items = this.items.filter(
                    (item) => item.public_id !== boardPublicId
                );

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = null;
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);
                invalidateRequestCache(
                    `taskboards:project:${board.project_public_id}`
                );
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {TaskAssignment} payload
         * @returns {Promise<TaskboardTaskRead | undefined>}
         * @throws {ApiError}
         */
        async addTask(boardPublicId, payload) {
            try {
                const task = await addTaskToBoard(boardPublicId, payload);

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: [...(this.currentTaskboard.tasks ?? []), task],
                    };
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);

                return task;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {number} taskPublicId
         * @throws {ApiError}
         */
        async removeTask(boardPublicId, taskPublicId) {
            try {
                await removeTaskFromBoard(boardPublicId, taskPublicId);

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: (this.currentTaskboard.tasks ?? []).filter(
                            (t) => t.task?.public_id !== taskPublicId
                        ),
                    };
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {number} taskPublicId
         * @param {TaskReposition} payload
         * @throws {ApiError}
         */
        async repositionTask(boardPublicId, taskPublicId, payload) {
            try {
                await repositionTask(boardPublicId, taskPublicId, payload);

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    const tasks = [...(this.currentTaskboard.tasks ?? [])];

                    const fromIndex = tasks.findIndex(
                        (entry) => entry.task?.public_id === taskPublicId
                    );

                    if (fromIndex !== -1) {
                        const [movedTask] = tasks.splice(fromIndex, 1);

                        tasks.splice(payload.position, 0, movedTask);

                        this.currentTaskboard = {
                            ...this.currentTaskboard,
                            tasks: tasks.map((entry, index) => ({
                                ...entry,
                                position: index,
                            })),
                        };
                    }
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);
            } catch (err) {
                throw err;
            }
        },
    },
});
