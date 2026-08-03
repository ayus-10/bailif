/**
 * @typedef {'active' | 'completed' | 'archived'} ProjectStatus
 */

/**
 * @typedef {'propose_only' | 'act_freely' | 'act_with_notify'} AgentPermissionLevel
 */

/**
 * @typedef {Object} ProjectRead
 * @property {string} id UUID
 *
 * @property {string} name
 * @property {string} description
 * @property {string} icon
 * @property {string | null} color
 * @property {ProjectStatus} status
 *
 * @property {string | null} start_date ISO datetime
 * @property {string | null} target_end_date ISO datetime
 * @property {string | null} actual_end_date ISO datetime
 * @property {string | null} timezone
 *
 * @property {boolean} agent_enabled
 * @property {AgentPermissionLevel} default_agent_permission_level
 * @property {Object} external_refs
 *
 * @property {string} created_at ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {string | null} archived_at ISO datetime
 */

/**
 * @typedef {Object} ProjectCreate
 * @property {string} name
 * @property {string} [description]
 * @property {string} [icon]
 * @property {string | null} [color]
 * @property {ProjectStatus} [status]
 *
 * @property {string | null} [start_date]
 * @property {string | null} [target_end_date]
 * @property {string | null} [actual_end_date]
 * @property {string | null} [timezone]
 *
 * @property {boolean} [agent_enabled]
 * @property {AgentPermissionLevel} [default_agent_permission_level]
 * @property {Object} [external_refs]
 */

/**
 * @typedef {Object} ProjectUpdate
 * @property {string} [name]
 * @property {string | null} [description]
 * @property {string | null} [icon]
 * @property {string | null} [color]
 * @property {ProjectStatus} [status]
 *
 * @property {string | null} [start_date]
 * @property {string | null} [target_end_date]
 * @property {string | null} [actual_end_date]
 * @property {string | null} [timezone]
 *
 * @property {boolean} [agent_enabled]
 * @property {AgentPermissionLevel} [default_agent_permission_level]
 * @property {Object | null} [external_refs]
 */

/**
 * @typedef {Object} ProjectFilterParams
 * @property {ProjectStatus} [status]
 * @property {boolean} [agent_enabled]
 * @property {string} [start_date_before]
 * @property {string} [start_date_after]
 * @property {string} [target_end_date_before]
 * @property {string} [target_end_date_after]
 * @property {boolean} [archived]
 * @property {string} [cursor]
 * @property {number} [limit]
 */

/**
 * @typedef {Object} ProjectListResponse
 * @property {ProjectRead[]} items
 * @property {string | null} next_cursor
 */

export {};
