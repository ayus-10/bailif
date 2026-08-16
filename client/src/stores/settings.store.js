import { defineStore } from "pinia";

export const useSettingsStore = defineStore("settings", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
