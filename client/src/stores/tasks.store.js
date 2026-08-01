import { defineStore } from "pinia";

import { fetchTasks } from "@/api/tasks.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const tasksResource = createResourceStore(
    /** @param {string} boardId */
    (boardId) => fetchTasks(boardId)
);

export const useTasksStore = defineStore("tasks", {
    state: () => tasksResource.state,
    actions: tasksResource.actions,
});
