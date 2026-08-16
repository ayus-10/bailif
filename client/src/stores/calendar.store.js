import { defineStore } from "pinia";

export const useCalendarStore = defineStore("calendar", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
