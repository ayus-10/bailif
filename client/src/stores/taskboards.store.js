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

/**
 * @typedef {import("@/api/shared.api").ApiError} ApiError
 * @typedef {import("@/types/taskboards").TaskboardRead} TaskboardRead
 * @typedef {import("@/types/taskboards").TaskboardListRead} TaskboardListRead
 * @typedef {import("@/types/taskboards").TaskboardCreate} TaskboardCreate
 * @typedef {import("@/types/taskboards").TaskboardUpdate} TaskboardUpdate
 * @typedef {import("@/types/taskboards").TaskAssignment} TaskAssignment
 * @typedef {import("@/types/taskboards").TaskReposition} TaskReposition
 * @typedef {import("@/types/taskboards").TaskboardTaskRead} TaskboardTaskRead
 * @typedef {import("@/types/taskboards").TaskboardsState} TaskboardsState
 * @typedef {import("@/types/shared").RequestStatus} RequestStatus
 */

/**
 * @param {string} operation
 * @param {...(number)} ids
 * @returns {string}
 */
function mutationKey(operation, ...ids) {
    return [operation, ...ids].join(":");
}

export const useTaskboardsStore = defineStore("taskboards", {
    /**
     * @returns {TaskboardsState}
     */
    state: () => ({
        items: [],
        currentTaskboard: null,
        fetchStatus: {},
        fetchErrors: {},
        mutationStatus: {},
        mutationErrors: {},
    }),

    actions: {
        /**
         * @param {Object} options
         * @param {number} options.projectPublicId
         * @param {boolean} [options.forceRefresh=false]
         * @throws {ApiError}
         */
        async fetch({ projectPublicId, forceRefresh = false }) {
            const key = `project:${projectPublicId}`;

            if (this.fetchStatus[key] === "loading" && !forceRefresh) {
                return;
            }

            this.fetchStatus[key] = "loading";
            this.fetchErrors[key] = null;

            const cacheKey = `taskboards:project:${projectPublicId}`;

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listTaskboards(projectPublicId),
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
         * @param {number} boardPublicId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<TaskboardRead | undefined>}
         * @throws {ApiError}
         */
        async get(boardPublicId, { forceRefresh = false } = {}) {
            const key = `taskboard:${boardPublicId}`;

            if (this.fetchStatus[key] === "loading" && !forceRefresh) {
                return;
            }

            this.fetchStatus[key] = "loading";
            this.fetchErrors[key] = null;

            try {
                const board = await cachedRequest(
                    key,
                    () => getTaskboard(boardPublicId),
                    { forceRefresh }
                );

                this.currentTaskboard = board;
                this.fetchStatus[key] = "success";

                return board;
            } catch (err) {
                this.fetchErrors[key] = err;
                this.fetchStatus[key] = "error";
                throw err;
            }
        },

        /**
         * @param {TaskboardCreate} payload
         * @returns {Promise<TaskboardRead>}
         * @throws {ApiError}
         */
        async create(payload) {
            const key = "create";

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                const board = await createTaskboard(payload);

                this.items = [...this.items, { ...board, task_count: 0 }]; // TODO: figure out if this is safe

                invalidateRequestCache(
                    `taskboards:project:${board.project_public_id}`
                );

                this.mutationStatus[key] = "success";

                return board;
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
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
            const key = mutationKey("update", boardPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                const index = this.items.findIndex(
                    (item) => item.public_id === boardPublicId
                );

                if (index === -1) {
                    this.mutationStatus[key] = "success";
                    return;
                }

                const board = await updateTaskboard(boardPublicId, payload);

                this.items = [
                    ...this.items.slice(0, index),
                    {
                        ...board,
                        task_count: this.items[index].task_count, // TODO: figure out if this is safe
                    },
                    ...this.items.slice(index + 1),
                ];

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = board;
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);
                invalidateRequestCache(
                    `taskboards:project:${board.project_public_id}`
                );

                this.mutationStatus[key] = "success";

                return board;
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @throws {ApiError}
         */
        async remove(boardPublicId) {
            const key = mutationKey("delete", boardPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                const board = this.items.find(
                    (item) => item.public_id === boardPublicId
                );

                if (!board) {
                    this.mutationStatus[key] = "success";
                    return;
                }

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

                this.mutationStatus[key] = "success";
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {TaskAssignment} payload
         * @returns {Promise<TaskboardTaskRead>}
         * @throws {ApiError}
         */
        async addTask(boardPublicId, payload) {
            const key = mutationKey("add-task", boardPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                const task = await addTaskToBoard(boardPublicId, payload);

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: [...(this.currentTaskboard.tasks ?? []), task],
                    };
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);

                this.mutationStatus[key] = "success";

                return task;
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
                throw err;
            }
        },

        /**
         * @param {number} boardPublicId
         * @param {number} taskPublicId
         * @throws {ApiError}
         */
        async removeTask(boardPublicId, taskPublicId) {
            const key = mutationKey("remove-task", boardPublicId, taskPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

            try {
                await removeTaskFromBoard(boardPublicId, taskPublicId);

                if (this.currentTaskboard?.public_id === boardPublicId) {
                    this.currentTaskboard = {
                        ...this.currentTaskboard,
                        tasks: (this.currentTaskboard.tasks ?? []).filter(
                            (task) => task.task?.public_id !== taskPublicId
                        ),
                    };
                }

                invalidateRequestCache(`taskboard:${boardPublicId}`);

                this.mutationStatus[key] = "success";
            } catch (err) {
                this.mutationStatus[key] = "error";
                this.mutationErrors[key] = err;
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
            const key = mutationKey("reposition", boardPublicId, taskPublicId);

            this.mutationStatus[key] = "loading";
            this.mutationErrors[key] = null;

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
         * @param {TaskboardsState} state
         * @returns {(projectPublicId: number) => RequestStatus | null}
         */
        fetchStatusByProject: (state) => (projectPublicId) => {
            return state.fetchStatus[`project:${projectPublicId}`] ?? null;
        },

        /**
         * @param {TaskboardsState} state
         * @returns {(projectPublicId: number) => unknown}
         */
        fetchErrorByProject: (state) => (projectPublicId) => {
            return state.fetchErrors[`project:${projectPublicId}`] ?? null;
        },

        /**
         * @param {TaskboardsState} state
         * @returns {(boardPublicId: number) => RequestStatus | null}
         */
        fetchStatusByBoard: (state) => (boardPublicId) => {
            return state.fetchStatus[`taskboard:${boardPublicId}`] ?? null;
        },

        /**
         * @param {TaskboardsState} state
         * @returns {(boardPublicId: number) => unknown}
         */
        fetchErrorByBoard: (state) => (boardPublicId) => {
            return state.fetchErrors[`taskboard:${boardPublicId}`] ?? null;
        },

        /**
         * @param {TaskboardsState} state
         * @returns {(operation: string, ...ids: (number)[]) => RequestStatus | null}
         */
        mutationStatusByKey:
            (state) =>
            (operation, ...ids) => {
                return (
                    state.mutationStatus[mutationKey(operation, ...ids)] ?? null
                );
            },

        /**
         * @param {TaskboardsState} state
         * @returns {(operation: string, ...ids: (number)[]) => unknown}
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
