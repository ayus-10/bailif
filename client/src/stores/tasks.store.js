import { defineStore } from "pinia";

import { listTasks, createTask, updateTask, deleteTask } from "@/api/tasks.api";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */

/** @typedef {"idle" | "loading" | "loading-more" | "success" | "error"} FetchStatus */

/**
 * @typedef {Object} TasksState
 * @property {Record<string, TaskRead[]>} items
 * @property {Record<string, string | null>} nextCursor
 * @property {Record<string, FetchStatus>} status
 * @property {Record<string, any>} errors
 */

export const useTasksStore = defineStore("tasks", {
    /** @returns {TasksState} */
    state: () => ({
        items: {},
        nextCursor: {},
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

        /** @param {string} boardId */
        loadMore(boardId) {
            const cursor = this.nextCursor[boardId];
            if (!cursor) return;

            return this.fetch(boardId, {
                cursor,
                append: true,
            });
        },

        /**
         * @param {string} boardId
         * @param {TaskCreate} payload
         * @returns {Promise<TaskRead>}
         */
        async create(boardId = "default", payload) {
            const task = await createTask({
                ...payload,
            });

            this.items[boardId] = [...(this.items[boardId] ?? []), task];

            return task;
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         * @param {Partial<TaskCreate>} payload
         * @returns {Promise<TaskRead>}
         */
        async update(boardId = "default", taskId, payload) {
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

            return task;
        },

        /**
         * @param {string} boardId
         * @param {string} taskId
         */
        async remove(boardId = "default", taskId) {
            await deleteTask(taskId);

            this.items[boardId] = (this.items[boardId] ?? []).filter(
                (item) => item.id !== taskId
            );
        },
    },
});
