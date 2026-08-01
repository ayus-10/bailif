import { defineStore } from "pinia";

import { fetchDocuments } from "@/api/documents.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const documentsResource = createResourceStore(
    /** @param {string} scopeId */
    (scopeId) => fetchDocuments(scopeId)
);

export const useDocumentsStore = defineStore("documents", {
    state: () => documentsResource.state,
    actions: documentsResource.actions,
});
