/**
 * @typedef {import("@/types/project").AgentPermissionLevel} AgentPermissionLevel
 * @typedef {import("@/types/project").ProjectStatus} ProjectStatus
 */

/**
 * @type {Array<{title: string, value: ProjectStatus}>}
 */
export const STATUS_ITEMS = [
    { title: "Active", value: "active" },
    { title: "On hold", value: "on_hold" },
    { title: "Completed", value: "completed" },
    { title: "Archived", value: "archived" },
];

/**
 * @type {Array<{title: string; value: AgentPermissionLevel, subtitle: string}>}
 */
export const PERMISSION_ITEMS = [
    {
        title: "Propose only",
        value: "propose_only",
        subtitle: "Agent suggests changes and you approve each one",
    },
    {
        title: "Act with notify",
        value: "act_with_notify",
        subtitle: "Agent makes changes and notifies you",
    },
    {
        title: "Act freely",
        value: "act_freely",
        subtitle: "Agent makes changes without asking",
    },
];

export const TIMEZONE_ITEMS =
    typeof Intl.supportedValuesOf === "function"
        ? Intl.supportedValuesOf("timeZone")
        : ["UTC"];
