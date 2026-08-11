import { defineStore } from "pinia";
import { fetchNotifications } from "@/api/notifications.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const notificationsResource = createResourceStore(
    /** @param {string} scopeId */
    (scopeId) => fetchNotifications(scopeId)
);

export const useNotificationsStore = defineStore("notifications", {
    state: () => notificationsResource.state,
    actions: notificationsResource.actions,
});
