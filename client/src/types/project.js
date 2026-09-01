/**
 * @typedef {'active' | 'on_hold' | 'completed' | 'archived'} ProjectStatus
 */

/**
 * @typedef {'propose_only' | 'act_freely' | 'act_with_notify'} AgentPermissionLevel
 */

/**
 * @typedef {Object} ProjectRead
 * @property {string} id
 * @property {string} name
 * @property {string} description
 * @property {string} icon
 * @property {string | null} color
 * @property {ProjectStatus} status
 * @property {string | null} start_date ISO datetime
 * @property {string | null} target_end_date ISO datetime
 * @property {string | null} actual_end_date ISO datetime
 * @property {string | null} timezone
 * @property {boolean} agent_enabled
 * @property {AgentPermissionLevel} default_agent_permission_level
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
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [target_end_date] ISO datetime
 * @property {string | null} [actual_end_date] ISO datetime
 * @property {string | null} [timezone]
 * @property {boolean} [agent_enabled]
 * @property {AgentPermissionLevel} [default_agent_permission_level]
 */

/**
 * @typedef {Object} ProjectUpdate
 * @property {string | null} [name]
 * @property {string | null} [description]
 * @property {string | null} [icon]
 * @property {string | null} [color]
 * @property {ProjectStatus | null} [status]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [target_end_date] ISO datetime
 * @property {string | null} [actual_end_date] ISO datetime
 * @property {string | null} [timezone]
 * @property {boolean | null} [agent_enabled]
 * @property {AgentPermissionLevel | null} [default_agent_permission_level]
 */

/**
 * @typedef {Object} ProjectFilterParams
 * @property {ProjectStatus | null} [status]
 * @property {boolean | null} [agent_enabled]
 * @property {string | null} [start_date_before] ISO datetime
 * @property {string | null} [start_date_after] ISO datetime
 * @property {string | null} [target_end_date_before] ISO datetime
 * @property {string | null} [target_end_date_after] ISO datetime
 * @property {boolean} [archived]
 */

/**
 * @typedef {Object} ProjectListResponse
 * @property {ProjectRead[]} items
 */

export {};
