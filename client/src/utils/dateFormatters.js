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
 * @param {string} iso
 */
export function isoToLocalInput(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return "";
    const pad = (/** @type {number} */ n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

/**
 * @param {string} value
 */
export function localInputToIso(value) {
    if (!value) return null;
    const d = new Date(value);
    return Number.isNaN(d.getTime()) ? null : d.toISOString();
}
