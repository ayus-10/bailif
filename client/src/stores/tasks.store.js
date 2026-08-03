import { defineStore } from "pinia";

import { listTasks } from "@/api/tasks.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const tasksResource = createResourceStore(
    /** @param {string} boardId */
    (boardId) => listTasks({})
);

export const useTasksStore = defineStore("tasks", {
    state: () => tasksResource.state,
    actions: tasksResource.actions,
});
