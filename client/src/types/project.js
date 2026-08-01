/**
 * @typedef {import('./task.js').Task} Task
 */

/**
 * @typedef {'active' | 'completed' | 'archived' | 'on_hold'} ProjectStatus
 */

/**
 * @typedef {'propose_only' | 'act_freely' | 'act_with_notify'} AgentPermissionLevel
 */

/**
 * @typedef {Object} Project
 * @property {string} id UUID
 *
 * // Core attributes
 * @property {string} name
 * @property {string} description
 * @property {string} icon
 * @property {string | null} color
 * @property {ProjectStatus} status
 *
 * // Scheduling
 * @property {string | null} start_date ISO datetime string
 * @property {string | null} target_end_date ISO datetime string
 * @property {string | null} actual_end_date ISO datetime string
 * @property {string | null} timezone
 *
 * // Agentic layer
 * @property {boolean} agent_enabled
 * @property {AgentPermissionLevel} default_agent_permission_level
 * @property {Object[]} agent_activity_log
 *
 * // Integrations
 * @property {Object.<string, any>} external_refs
 *
 * // Relations
 * @property {Task[]} tasks
 *
 * // Embedding
 * @property {number[] | null} embedding
 *
 * // Timestamps
 * @property {string} created_at ISO datetime string
 * @property {string} updated_at ISO datetime string
 * @property {string | null} archived_at ISO datetime string
 */

export {};
