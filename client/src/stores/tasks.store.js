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
 * @param {number} projectPublicId
 * @param {TaskFetchOptions} options
 * @returns {string}
 */
function collectionKey(projectPublicId, options = {}) {
    const {
        parentId = null,
        taskboardId = null,
        status = null,
        priority = null,
        type = null,
        tag = null,
        dueBefore = null,
        dueAfter = null,
    } = options;

    const queryMode = parentId ? "child-tasks" : "root-tasks";

    return [
        projectPublicId,
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
         * @param {number} projectPublicId
         * @param {TaskFetchOptions} [options]
         */
        async fetch(
            projectPublicId,
            {
                queryMode = "root-tasks",
                parentId = null,
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
            if (projectPublicId == null) {
                throw new Error("projectPublicId is required");
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

            const key = collectionKey(projectPublicId, query);

            if (this.status[key] === "loading" && !forceRefresh) {
                return;
            }

            this.status[key] = append ? "loading-more" : "loading";
            this.errors[key] = null;

            const params = {
                cursor,
                ...(queryMode === "child-tasks" && parentId
                    ? { parent_public_id: parentId }
                    : { only_root: true }),
                ...(taskboardId != null
                    ? { taskboard_public_id: taskboardId }
                    : {}),
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

                this.nextCursor[key] = data.next_cursor ?? null;
                this.queries[key] = query;
                this.status[key] = "success";

                return data;
            } catch (err) {
                this.errors[key] = err;
                this.status[key] = "error";
            }
        },

        /**
         * @param {number} projectPublicId
         * @param {TaskFetchOptions} [options]
         */
        async loadMore(projectPublicId, options = {}) {
            const key = collectionKey(projectPublicId, options);
            const cursor = this.nextCursor[key];

            if (!cursor) {
                return;
            }

            return this.fetch(projectPublicId, {
                ...options,
                cursor,
                append: true,
            });
        },

        /**
         * @param {number} taskPublicId
         * @param {Object} [options]
         * @param {boolean} [options.forceRefresh=false]
         * @returns {Promise<TaskRead | undefined>}
         */
        async get(taskPublicId, { forceRefresh = false } = {}) {
            try {
                const task = await cachedRequest(
                    `task:${taskPublicId}`,
                    () => getTask(taskPublicId),
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
         * @throws {Error}
         */
        async create(payload) {
            try {
                const task = await createTask(payload);
                const projectPublicId = task.project_public_id;

                invalidateRequestCache(`tasks:${projectPublicId}:`);

                const rootKey = collectionKey(projectPublicId, {
                    queryMode: task.parent_public_id
                        ? "child-tasks"
                        : "root-tasks",
                    parentId: task.parent_public_id ?? undefined,
                });

                if (this.items[rootKey]) {
                    this.items[rootKey] = [...this.items[rootKey], task];
                }

                return task;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} taskPublicId
         * @param {TaskUpdate} payload
         * @returns {Promise<TaskRead | undefined>}
         * @throws {Error}
         */
        async update(taskPublicId, payload) {
            try {
                const task = await updateTask(taskPublicId, payload);

                if (task.public_id === this.currentTask?.public_id) {
                    this.currentTask = task;
                }

                for (const key of Object.keys(this.items)) {
                    const tasks = this.items[key];
                    const index = tasks.findIndex(
                        (item) => item.public_id === taskPublicId
                    );

                    if (index === -1) {
                        continue;
                    }

                    this.items[key] = [
                        ...tasks.slice(0, index),
                        task,
                        ...tasks.slice(index + 1),
                    ];
                }

                invalidateRequestCache(`task:${taskPublicId}`);
                invalidateRequestCache(`tasks:${task.project_public_id}:`);

                return task;
            } catch (err) {
                throw err;
            }
        },

        /**
         * @param {number} taskPublicId
         * @param {number} projectPublicId
         * @throws {Error}
         */
        async remove(taskPublicId, projectPublicId) {
            if (projectPublicId == null) {
                throw new Error("projectPublicId is required");
            }

            try {
                await deleteTask(taskPublicId);

                for (const key of Object.keys(this.items)) {
                    this.items[key] = this.items[key].filter(
                        (item) => item.public_id !== taskPublicId
                    );
                }

                if (this.currentTask?.public_id === taskPublicId) {
                    this.currentTask = null;
                }

                invalidateRequestCache(`task:${taskPublicId}`);
                invalidateRequestCache(`tasks:${projectPublicId}:`);
            } catch (err) {
                throw err;
            }
        },
    },

    getters: {
        /**
         * @param {TasksState} state
         * @returns {(projectPublicId: number, options?: TaskFetchOptions) => TaskRead[]}
         */
        tasksByQuery:
            (state) =>
            (projectPublicId, options = {}) => {
                const key = collectionKey(projectPublicId, options);

                return state.items[key] ?? [];
            },

        /**
         * @param {TasksState} state
         * @returns {(projectPublicId: number, options?: TaskFetchOptions) => FetchStatus | null}
         */
        statusByQuery:
            (state) =>
            (projectPublicId, options = {}) => {
                const key = collectionKey(projectPublicId, options);

                return state.status[key] ?? null;
            },

        /**
         * @param {TasksState} state
         * @returns {(projectPublicId: number, options?: TaskFetchOptions) => unknown}
         */
        errorByQuery:
            (state) =>
            (projectPublicId, options = {}) => {
                const key = collectionKey(projectPublicId, options);

                return state.errors[key] ?? null;
            },
    },
});
