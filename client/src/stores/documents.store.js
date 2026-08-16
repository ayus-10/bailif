import { defineStore } from "pinia";

export const useDocumentsStore = defineStore("documents", {
    state: () => ({
        items: {},
        status: {},
        errors: {},
    }),
    actions: {
        fetch() {},
    },
});
