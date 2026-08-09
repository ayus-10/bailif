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

/** @typedef {import('@/types/task').TaskType} TaskType */

export const TYPE_ICONS =
    /** @type {Record<TaskType, string>} */
    ({
        bug: "mdi-bug-outline",
        task: "mdi-star-outline",
        subtask: "mdi-checkbox-marked-circle-outline",
        epic: "mdi-flag-outline",
    });

export const TYPE_LABELS =
    /** @type {Record<TaskType, string>} */
    ({
        bug: "Bug",
        task: "Task",
        subtask: "Subtask",
        epic: "Epic",
    });

export const FALLBACK_STATUS_META = {
    color: "grey",
    icon: "mdi-help-circle-outline",
};

export const FALLBACK_TYPE_ICON = "mdi-checkbox-blank-circle-outline";
