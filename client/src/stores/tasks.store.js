import { defineStore } from "pinia";
import {
    createTask,
    deleteTask,
    getTask,
    listTasks,
    updateTask,
} from "@/api/tasks.api";
import { cachedRequest, invalidateRequestCache } from "./cache";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskCreate} TaskCreate */
/** @typedef {import("@/types/task").TaskUpdate} TaskUpdate */
/** @typedef {import("@/types/task").TaskListParams} TaskListParams */
/** @typedef {import("@/types/task").TaskFetchOptions} TaskFetchOptions */
/** @typedef {import("@/types/task").TasksState} TasksState */
/** @typedef {import("@/types/shared").FetchStatus} FetchStatus */

/**
 * @param {string} projectId
 * @param {TaskFetchOptions} options
 * @returns {string}
 */
function collectionKey(projectId, options = {}) {
    const {
        queryMode = "root-tasks",
        parentId = null,
        taskboardId = null,
        status = null,
        priority = null,
        type = null,
        tag = null,
        dueBefore = null,
        dueAfter = null,
    } = options;

    return [
        projectId,
        queryMode,
        parentId ?? "root",
        taskboardId ?? "all",
        status ?? "all",
        priority ?? "all",
        type ?? "all",
        tag ?? "all",
        dueBefore ?? "none",
        dueAfter ?? "none",
    ].join(":");
}

export const useTasksStore = defineStore("tasks", {
    /** @returns {TasksState} */
    state: () => ({
        items: {},
        nextCursor: {},
        queries: {},
        currentTask: null,
        status: {},
        errors: {},
    }),

    actions: {
        /**
         * @param {string} projectId
         * @param {TaskFetchOptions} [options]
         */
        async fetch(
            projectId,
            {
                queryMode = "root-tasks",
                parentId,
                taskboardId = null,
                status = null,
                priority = null,
                type = null,
                tag = null,
                dueBefore = null,
                dueAfter = null,
                cursor = null,
                append = false,
                forceRefresh = false,
            } = {}
        ) {
            if (!projectId) {
                throw new Error("projectId is required");
            }

            if (queryMode === "child-tasks" && !parentId) {
                throw new Error(
                    "parentId is required when queryMode is 'child-tasks'"
                );
            }

            const query = {
                queryMode,
                parentId,
                taskboardId,
                status,
                priority,
                type,
                tag,
                dueBefore,
                dueAfter,
                cursor,
                append,
                forceRefresh,
            };

            const key = collectionKey(projectId, query);

            if (this.status[key] === "loading" && !forceRefresh) {
                return;
            }

            this.status[key] = append ? "loading-more" : "loading";
            this.errors[key] = null;

            const params = {
                project_id: projectId,
                cursor,
                ...(queryMode === "child-tasks"
                    ? { parent_id: parentId }
                    : { only_root: true }),
                ...(taskboardId != null ? { taskboard_id: taskboardId } : {}),
                ...(status != null ? { status } : {}),
                ...(priority != null ? { priority } : {}),
                ...(type != null ? { type } : {}),
                ...(tag != null ? { tag } : {}),
                ...(dueBefore != null ? { due_before: dueBefore } : {}),
                ...(dueAfter != null ? { due_after: dueAfter } : {}),
            };

            try {
                const data = await cachedRequest(
                    `tasks:${key}:${cursor ?? "first"}`,
                    () => listTasks(/** @type {TaskListParams} */ (params)),
                    { forceRefresh }
                );

                const existing = this.items[key] ?? [];

                this.items[key] = append
                    ? [...existing, ...data.items]
                    : data.items;

                this.nextCursor[key] = data.next_cursor;
                this.queries[key] = query;
                this.status[key] = "success";

                return data;
            } catch (err) {
                this.errors[key] = err;
                this.status[key] = "error";
            }
        },

        /**
         * @param {string} projectId
         * @param {TaskFetchOptions} [options]
         */
        async loadMore(projectId, options = {}) {
            const key = collectionKey(projectId, options);
            const cursor = this.nextCursor[key];

            if (!cursor) {
                return;
            }

            return this.fetch(projectId, {
                ...options,
                cursor,
                append: true,
            });
        },

        /**
         * @param {string} taskId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<TaskRead | undefined>}
         */
        async get(taskId, { forceRefresh = false } = {}) {
            try {
                const task = await cachedRequest(
                    `task:${taskId}`,
                    () => getTask(taskId),
                    { forceRefresh }
                );

                this.currentTask = task;

                return task;
            } catch (err) {
                this.errors.task = err;
                this.status.task = "error";
            }
        },

        /**
         * @param {TaskCreate} payload
         * @returns {Promise<TaskRead | undefined>}
         */
        async create(payload) {
            const projectId = payload?.project_id;

            if (!projectId) {
                throw new Error("project_id is required");
            }

            try {
                const task = await createTask(payload);

                invalidateRequestCache(`tasks:${projectId}:`);

                const rootKey = collectionKey(projectId, {
                    queryMode: task.parent_id ? "child-tasks" : "root-tasks",
                    parentId: task.parent_id ?? undefined,
                });

                if (this.items[rootKey]) {
                    this.items[rootKey] = [...this.items[rootKey], task];
                }

                return task;
            } catch (err) {
                const key = projectId ?? "unknown";

                this.errors[key] = err;
                this.status[key] = "error";
            }
        },

        /**
         * @param {string} taskId
         * @param {TaskUpdate} payload
         * @returns {Promise<TaskRead | undefined>}
         */
        async update(taskId, payload) {
            const projectId = payload?.project_id;

            if (!projectId) {
                throw new Error("project_id is required");
            }

            try {
                const task = await updateTask(taskId, payload);

                if (task.id === this.currentTask?.id) {
                    this.currentTask = task;
                }

                for (const key of Object.keys(this.items)) {
                    const tasks = this.items[key];
                    const index = tasks.findIndex((item) => item.id === taskId);

                    if (index === -1) {
                        continue;
                    }

                    this.items[key] = [
                        ...tasks.slice(0, index),
                        task,
                        ...tasks.slice(index + 1),
                    ];
                }

                invalidateRequestCache(`task:${taskId}`);
                invalidateRequestCache(`tasks:${projectId}:`);

                return task;
            } catch (err) {
                this.errors[projectId] = err;
                this.status[projectId] = "error";
            }
        },

        /**
         * @param {string} taskId
         * @param {string} projectId
         */
        async remove(taskId, projectId) {
            if (!projectId) {
                throw new Error("projectId is required");
            }

            try {
                await deleteTask(taskId);

                for (const key of Object.keys(this.items)) {
                    this.items[key] = this.items[key].filter(
                        (item) => item.id !== taskId
                    );
                }

                if (this.currentTask?.id === taskId) {
                    this.currentTask = null;
                }

                invalidateRequestCache(`task:${taskId}`);
                invalidateRequestCache(`tasks:${projectId}:`);
            } catch (err) {
                this.errors[projectId] = err;
                this.status[projectId] = "error";
            }
        },
    },
});
