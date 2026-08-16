import { defineStore } from "pinia";

export const useGanttStore = defineStore("gantt", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
