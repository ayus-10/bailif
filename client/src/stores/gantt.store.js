import { defineStore } from "pinia";

import { fetchGantt } from "@/api/gantt.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const ganttResource = createResourceStore(
    /** @param {string} projectId */
    (projectId) => fetchGantt(projectId)
);

export const useGanttStore = defineStore("gantt", {
    state: () => ganttResource.state,
    actions: ganttResource.actions,
});
