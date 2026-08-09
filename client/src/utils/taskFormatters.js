/** @typedef {import('@/types/task').TaskRead} TaskRead */

/**
 * @param {string | null | undefined} iso
 * @returns {string | null}
 */
export function formatDate(iso) {
    if (!iso) return null;
    return new Date(iso).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
    });
}

/**
 * @param {number | null | undefined} minutes
 * @returns {string | null}
 */
export function formatDuration(minutes) {
    if (!minutes) return null;
    if (minutes < 60) return `${minutes}m`;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m ? `${h}h ${m}m` : `${h}h`;
}

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
