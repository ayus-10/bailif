import { defineStore } from "pinia";

export const useNotificationsStore = defineStore("notifications", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
