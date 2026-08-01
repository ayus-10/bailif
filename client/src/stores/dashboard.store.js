import { defineStore } from "pinia";

import { fetchDashboard } from "@/api/dashboard.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const dashboardResource = createResourceStore(
    /**
     * @param {string} scopeId
     * @param {AbortSignal} signal
     */

    (scopeId, signal) => fetchDashboard(scopeId, signal)
);

export const useDashboardStore = defineStore("dashboard", {
    state: () => dashboardResource.state,
    actions: dashboardResource.actions,
});
