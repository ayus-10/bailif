import { defineStore } from "pinia";
import { fetchSettings } from "@/api/settings.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const settingsResource = createResourceStore(
    /** @param {string} scopeId */
    (scopeId) => fetchSettings(scopeId)
);

export const useSettingsStore = defineStore("settings", {
    state: () => settingsResource.state,
    actions: settingsResource.actions,
});
