/**
 * @typedef {Object} ColorOption
 * @property {string} label
 * @property {string} value
 */

/**
 * @typedef {Object} IconOption
 * @property {string} label
 * @property {string} value
 */

/** @type {ColorOption[]} */
export const DEFAULT_COLORS = [
    { label: "Iris", value: "#6366F1" },
    { label: "Violet", value: "#8B5CF6" },
    { label: "Fuchsia", value: "#EC4899" },
    { label: "Ember", value: "#EF4444" },
    { label: "Tangerine", value: "#F97316" },
    { label: "Saffron", value: "#EAB308" },
    { label: "Jade", value: "#22C55E" },
    { label: "Lagoon", value: "#14B8A6" },
    { label: "Aqua", value: "#06B6D4" },
    { label: "Cobalt", value: "#3B82F6" },
];

/** @type {IconOption[]} */
export const DEFAULT_ICONS = [
    { label: "Home", value: "mdi-home" },
    { label: "Folder", value: "mdi-folder" },
    { label: "Calendar", value: "mdi-calendar" },
    { label: "Check", value: "mdi-check-circle" },
    { label: "Star", value: "mdi-star" },
    { label: "Heart", value: "mdi-heart" },
    { label: "Flag", value: "mdi-flag" },
    { label: "Bell", value: "mdi-bell" },
    { label: "Bookmark", value: "mdi-bookmark" },
    { label: "Lightning", value: "mdi-lightning-bolt" },
];
