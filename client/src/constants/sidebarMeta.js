/** @typedef {import('@/types/task.js').TaskStatus} TaskStatusValue */
/** @typedef {import('@/types/task.js').TaskPriority} TaskPriorityValue */

/**
 * @typedef {Object} TaskStatusOption
 * @property {TaskStatusValue} value
 * @property {string} label
 * @property {string} icon
 */

/**
 * @typedef {Object} TaskPriorityOption
 * @property {TaskPriorityValue} value
 * @property {string} label
 * @property {string} color
 */

/** @type {TaskStatusOption[]} */
export const taskStatuses = [
    { value: "open", label: "Open", icon: "mdi-circle-outline" },
    { value: "in_progress", label: "In Progress", icon: "mdi-progress-clock" },
    { value: "done", label: "Done", icon: "mdi-check-circle-outline" },
];

/** @type {TaskPriorityOption[]} */
export const taskPriorities = [
    { value: "low", label: "Low", color: "success" },
    { value: "medium", label: "Medium", color: "warning" },
    { value: "high", label: "High", color: "error" },
];
