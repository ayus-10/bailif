export const TASK_COLUMNS = [
    {
        status: "todo",
        label: "To Do",
        icon: "mdi-circle-outline",
    },
    {
        status: "in-progress",
        label: "In Progress",
        icon: "mdi-progress-clock",
    },
    {
        status: "done",
        label: "Done",
        icon: "mdi-check-circle-outline",
    },
];

/** @type {Record<string, string>} */
export const PRIORITY_COLORS = {
    low: "success",
    medium: "warning",
    high: "error",
};
