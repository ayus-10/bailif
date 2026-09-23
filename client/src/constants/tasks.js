/**
 * @typedef {import("@/types/task").TaskType} TaskType
 * @typedef {import("@/types/task").TaskPriority} TaskPriority
 * @typedef {import("@/types/task").TaskStatus} TaskStatus
 */

/**
 * @typedef {Object} StatusSwatch
 * @property {string} label
 * @property {string} value
 */

/**
 * @typedef {Object} StatusMeta
 * @property {TaskStatus} status
 * @property {string} label
 * @property {string} icon
 * @property {string} emptyLabel
 * @property {StatusSwatch} color
 */

/**
 * @typedef {Object} PriorityMeta
 * @property {string} label
 * @property {string} icon
 * @property {string} color
 */

/**
 * @type {StatusMeta[]}
 */
export const STATUS_META = [
    {
        status: "open",
        label: "Open",
        emptyLabel: "No open tasks",
        icon: "mdi-circle-outline",
        color: { label: "Slate", value: "#64748B" },
    },
    {
        status: "in_progress",
        label: "In Progress",
        emptyLabel: "No tasks in progress",
        icon: "mdi-progress-clock",
        color: { label: "Blue", value: "#3B82F6" },
    },
    {
        status: "in_review",
        label: "In Review",
        emptyLabel: "No tasks in review",
        icon: "mdi-eye-outline",
        color: { label: "Purple", value: "#8B5CF6" },
    },
    {
        status: "done",
        label: "Done",
        emptyLabel: "No completed tasks",
        icon: "mdi-check-circle-outline",
        color: { label: "Green", value: "#22C55E" },
    },
    {
        status: "blocked",
        label: "Blocked",
        emptyLabel: "No blocked tasks",
        icon: "mdi-block-helper",
        color: { label: "Orange", value: "#F97316" },
    },
    {
        status: "cancelled",
        label: "Cancelled",
        emptyLabel: "No cancelled tasks",
        icon: "mdi-close-circle-outline",
        color: { label: "Red", value: "#EF4444" },
    },
];

/**
 * @type {Record<TaskPriority, PriorityMeta>}
 */
export const PRIORITY_META = {
    low: {
        label: "Low",
        icon: "mdi-circle-outline",
        color: "success",
    },
    medium: {
        label: "Medium",
        icon: "mdi-circle-half-full",
        color: "warning",
    },
    high: {
        label: "High",
        icon: "mdi-circle",
        color: "error",
    },
};
