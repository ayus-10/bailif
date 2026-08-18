/** @typedef {import("@/types/task").TaskPriority} TaskPriority */
/** @typedef {import("@/types/task").TaskStatus} TaskStatus */

/** @type {{ status: TaskStatus; label: string; icon: string }[]} */
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
        status: "in_review",
        label: "In Review",
        icon: "mdi-eye-outline",
    },
    {
        status: "done",
        label: "Done",
        icon: "mdi-check-circle-outline",
    },
    {
        status: "blocked",
        label: "Blocked",
        icon: "mdi-block-helper",
    },
    {
        status: "cancelled",
        label: "Cancelled",
        icon: "mdi-close-circle-outline",
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
