import { defineStore } from "pinia";

import { listTasks } from "@/api/tasks.api";

/**
 * @typedef {import('@/types/task').TaskRead} TaskRead
 */

/**
 * @typedef {"idle" | "loading" | "loading-more" | "success" | "error"} FetchStatus
 */

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
            return this.fetch(boardId, { cursor, append: true });
        },
    },
});
