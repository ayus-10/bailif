import { defineStore } from "pinia";
import {
    createTask,
    deleteTask,
    getTask,
    listTasks,
    updateTask,
} from "@/api/tasks.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

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
         * @param {"root-tasks" | "child-tasks"} [options.queryMode="root-tasks"]
         * @param {string} [options.parentId]
         * @param {string | null} [options.cursor=null]
         * @param {boolean} [options.append=false]
         * @param {boolean} [options.forceRefresh=false]
         */
        async fetch(
            boardId,
            {
                queryMode = "root-tasks",
                parentId,
                cursor = null,
                append = false,
                forceRefresh = false,
            } = {}
        ) {
            if (this.status[boardId] === "loading" && !forceRefresh) return;

            if (queryMode === "child-tasks" && !parentId) {
                throw new Error(
                    "parentId is required when queryMode is 'child-tasks'"
                );
            }

            /** @type Record<string, any> */
            const params = { cursor };
            if (queryMode === "child-tasks") {
                params.parent_id = parentId;
            } else {
                params.only_root = true;
            }

            this.status[boardId] = append ? "loading-more" : "loading";
            this.errors[boardId] = null;

            const cacheKey = [
                "tasks",
                boardId,
                cursor ?? "first",
                queryMode,
                queryMode === "child-tasks" ? parentId : "root",
            ].join(":");

            try {
                const data = await cachedRequest(
                    cacheKey,
                    () => listTasks(params),
                    { forceRefresh }
                );
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
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         */
        async get(boardId = "default", taskId, { forceRefresh = false } = {}) {
            try {
                const task = await cachedRequest(
                    `task:${taskId}`,
                    () => getTask(taskId),
                    { forceRefresh }
                );

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

                invalidateRequestCache(`tasks:${boardId}:`);

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

                invalidateRequestCache(`task:${taskId}`);
                invalidateRequestCache(`tasks:${boardId}:`);

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

                invalidateRequestCache(`task:${taskId}`);
                invalidateRequestCache(`tasks:${boardId}:`);
            } catch (err) {
                this.errors[boardId] = err;
                this.status[boardId] = "error";
            }
        },
    },
});
