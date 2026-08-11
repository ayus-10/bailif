/** @typedef {import("@/components/tasks/PendingTaskCard.vue").TaskPriority} TaskPriority */

export const TASK_COLUMNS = [
    {
        status: "open",
        label: "Open",
        icon: "mdi-circle-outline",
    },
    {
        status: "in_progress",
        label: "In Progress",
        icon: "mdi-progress-clock",
    },
    {
        status: "done",
        label: "Done",
        icon: "mdi-check-circle-outline",
    },
];

/** @type {Record<TaskPriority, string>} */
export const PRIORITY_COLORS = {
    low: "success",
    medium: "warning",
    high: "error",
};

/** @type {Record<TaskPriority, string>} */
export const PRIORITY_ICONS = {
    low: "mdi-arrow-down",
    medium: "mdi-minus",
    high: "mdi-arrow-up",
};
