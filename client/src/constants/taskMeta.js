/** @typedef {import('@/types/task').TaskType} TaskType */
/** @typedef {import('@/types/task').TaskPriority} TaskPriority */

/** @type {TaskPriority[]} */
export const TASK_PRIORITIES = ["low", "medium", "high"];

export const STATUS_META = {
    open: { color: "grey", icon: "mdi-circle-outline", label: "Open" },
    in_progress: {
        color: "blue",
        icon: "mdi-progress-clock",
        label: "In progress",
    },
    in_review: { color: "purple", icon: "mdi-eye-outline", label: "In review" },
    done: { color: "success", icon: "mdi-check-circle", label: "Done" },
    blocked: { color: "error", icon: "mdi-block-helper", label: "Blocked" },
    cancelled: {
        color: "grey-darken-1",
        icon: "mdi-close-circle-outline",
        label: "Cancelled",
    },
};
