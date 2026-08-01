import { defineStore } from "pinia";

import { fetchCalendar } from "@/api/calendar.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const calendarResource = createResourceStore(
    /**
     * @param {string} monthKey
     * @param {AbortSignal} signal
     */
    (monthKey, signal) => fetchCalendar(monthKey, signal)
);

export const useCalendarStore = defineStore("calendar", {
    state: () => calendarResource.state,
    actions: calendarResource.actions,
});
