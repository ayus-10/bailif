import { defineStore } from "pinia";

export const useDashboardStore = defineStore("dashboard", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
