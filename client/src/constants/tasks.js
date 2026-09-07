/** @typedef {import("@/types/task").TaskPriority} TaskPriority */
/** @typedef {import("@/types/task").TaskStatus} TaskStatus */

/**
 * @typedef {Object} TaskColumnConfig
 * @property {TaskStatus} status
 * @property {string} label
 * @property {string} icon
 * @property {TaskColumnColor} color
 * @property {string} emptyLabel
 */

/**
 * @typedef {Object} TaskColumnColor
 * @property {string} label
 * @property {string} value
 */

/** @type {TaskColumnConfig[]} */
export const TASK_COLUMNS = [
    {
        status: "open",
        label: "Open",
        emptyLabel: "No open tasks",
        icon: "mdi-circle-outline",
        color: {
            label: "Slate",
            value: "#64748B",
        },
    },
    {
        status: "in_progress",
        label: "In Progress",
        emptyLabel: "No tasks in progress",
        icon: "mdi-progress-clock",
        color: {
            label: "Blue",
            value: "#3B82F6",
        },
    },
    {
        status: "in_review",
        label: "In Review",
        emptyLabel: "No tasks in review",
        icon: "mdi-eye-outline",
        color: {
            label: "Purple",
            value: "#8B5CF6",
        },
    },
    {
        status: "done",
        label: "Done",
        emptyLabel: "No completed tasks",
        icon: "mdi-check-circle-outline",
        color: {
            label: "Green",
            value: "#22C55E",
        },
    },
    {
        status: "blocked",
        label: "Blocked",
        emptyLabel: "No blocked tasks",
        icon: "mdi-block-helper",
        color: {
            label: "Orange",
            value: "#F97316",
        },
    },
    {
        status: "cancelled",
        label: "Cancelled",
        emptyLabel: "No cancelled tasks",
        icon: "mdi-close-circle-outline",
        color: {
            label: "Red",
            value: "#EF4444",
        },
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
