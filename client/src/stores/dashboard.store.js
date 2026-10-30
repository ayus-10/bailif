import { defineStore } from "pinia";
import { fetchDashboard } from "@/api/dashboard.api";

/**
 * @typedef {import("@/api/shared.api").ApiError} ApiError
 * @typedef {import("@/types/dashboard").DashboardState} DashboardState
 */

export const useDashboardStore = defineStore("dashboard", {
    /**
     * @returns {DashboardState}
     */
    state: () => ({
        data: null,
        status: null,
        error: null,
    }),

    actions: {
        /**
         * @throws {ApiError}
         */
        async fetch() {
            if (this.status === "loading") {
                return;
            }

            this.status = "loading";
            this.error = null;

            try {
                this.data = await fetchDashboard();
                this.status = "success";
            } catch (err) {
                this.error = err;
                this.status = "error";
                throw err;
            }
        },
    },
});
