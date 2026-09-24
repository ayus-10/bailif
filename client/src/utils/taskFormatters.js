/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 */

/**
 * @param {TaskRead} task
 * @returns {boolean}
 */
export function isTaskOverdue(task) {
    if (!task.due_date) return false;
    if (["done", "cancelled"].includes(task.status)) return false;
    return new Date(task.due_date) < new Date();
}

/**
 * @param {string | null | undefined} tags
 * @returns {string[]}
 */
export function parseTags(tags) {
    return (tags ?? "")
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);
}

/**
 * @param {string[] | null | undefined} tags
 * @returns {string}
 */
export function serializeTags(tags) {
    return (tags ?? [])
        .map((t) => t.trim())
        .filter(Boolean)
        .join(", ");
}
