import { defineStore } from "pinia";
import {
    createTask,
    deleteTask,
    getTask,
    listTasks,
    updateTask,
} from "@/api/tasks.api";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */

/** @typedef {import('@/types/shared').FetchStatus} FetchStatus */

/**
 * @typedef {Object} TasksState
 * @property {Record<string, TaskRead[]>} items
 * @property {Record<string, string | null>} nextCursor
 * @property {TaskRead | null} currentTask
 * @property {Record<string, FetchStatus>} status
 * @property {Record<string, any>} errors
 */

export const useTasksStore = defineStore("tasks", {
    /** @returns {TasksState} */
    state: () => ({
        items: {},
        nextCursor: {},
        currentTask: null,
        status: {},
        errors: {},
    }),

    actions: {
        /**
         * @param {string} boardId
         * @param {Object} [options]
         * @param {?string} [options.cursor=null]
         * @param {boolean} [options.append=false]
         * @param {boolean} [options.force=false]
         */
        async fetch(
            boardId,
            { cursor = null, append = false, force = false } = {}
        ) {
            if (this.status[boardId] === "loading" && !force) return;

            this.status[boardId] = append ? "loading-more" : "loading";
            this.errors[boardId] = null;

            try {
                const data = await listTasks({ cursor });

                this.items[boardId] = append
                    ? [...(this.items[boardId] ?? []), ...data.items]
                    : data.items;

                this.nextCursor[boardId] = data.next_cursor;
                this.status[boardId] = "success";
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },

        /**
         * @param {String} boardId
         */
        loadMore(boardId) {
            try {
                const cursor = this.nextCursor[boardId];

                if (!cursor) return;

                return this.fetch(boardId, {
                    cursor,
                    append: true,
                });
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         */
        async get(boardId = "default", taskId) {
            try {
                const task = await getTask(taskId);

                this.currentTask = task;

                return task;
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {TaskCreate} payload
         * @returns {Promise<TaskRead | undefined>}
         */
        async create(boardId = "default", payload) {
            try {
                const task = await createTask({
                    ...payload,
                });

                this.items[boardId] = [...(this.items[boardId] ?? []), task];

                return task;
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         * @param {Partial<TaskCreate>} payload
         * @returns {Promise<TaskRead | undefined>}
         */
        async update(boardId = "default", taskId, payload) {
            try {
                const task = await updateTask(taskId, payload);

                const tasks = this.items[boardId] ?? [];
                const index = tasks.findIndex((item) => item.id === taskId);

                if (index !== -1) {
                    this.items[boardId] = [
                        ...tasks.slice(0, index),
                        task,
                        ...tasks.slice(index + 1),
                    ];
                }

                if (task.id === this.currentTask?.id) {
                    this.currentTask = task;
                }

                return task;
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         */
        async remove(boardId = "default", taskId) {
            try {
                await deleteTask(taskId);

                this.items[boardId] = (this.items[boardId] ?? []).filter(
                    (item) => item.id !== taskId
                );
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },
    },
});
