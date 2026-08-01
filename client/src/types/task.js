/**
 * @typedef {import('./project.js').Project} Project
 */

/**
 * @typedef {'low' | 'medium' | 'high'} TaskPriority
 */

/**
 * @typedef {'open' | 'in_progress' | 'done'} TaskStatus
 */

/**
 * @typedef {'task' | 'subtask' | 'epic' | 'bug'} TaskType
 */

/**
 * @typedef {'human' | 'agent'} CreatedBy
 */

/**
 * @typedef {'none' | 'pending' | 'approved' | 'rejected'} ApprovalStatus
 */

/**
 * @typedef {'propose_only' | 'act_freely' | 'act_with_notify'} AgentPermissionLevel
 */

/**
 * @typedef {'blocks' | 'blocked_by' | 'relates_to'} DependencyType
 */

/**
 * @typedef {Object} Task
 * @property {string} id UUID
 *
 * // Core attributes
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus} status
 * @property {TaskPriority} priority
 * @property {TaskType} type
 * @property {string} tags Comma-separated tags
 *
 * // Scheduling
 * @property {string | null} start_date ISO datetime string
 * @property {string | null} due_date ISO datetime string
 * @property {number | null} estimated_duration_minutes
 * @property {string | null} timezone
 * @property {string | null} recurrence_rule RRULE string
 *
 * // Hierarchy
 * @property {string | null} parent_id UUID of parent task
 * @property {Task[]} subtasks
 *
 * // Dependencies
 * @property {TaskDependency[]} outgoing_dependencies
 *
 * // Project
 * @property {string | null} project_id UUID
 * @property {Project | null} project
 *
 * // Agentic layer
 * @property {CreatedBy} created_by
 * @property {ApprovalStatus} approval_status
 * @property {AgentPermissionLevel | null} agent_permission_level
 * @property {Object[]} agent_activity_log
 * @property {string | null} reasoning_trace
 *
 * // Embedding
 * @property {number[] | null} embedding
 *
 * // Timestamps
 * @property {string} created_at ISO datetime string
 * @property {string} updated_at ISO datetime string
 */

/**
 * @typedef {Object} TaskDependency
 * @property {string} id UUID
 * @property {string} task_id UUID
 * @property {string} depends_on_id UUID
 * @property {DependencyType} dependency_type
 *
 * // Relations
 * @property {Task} task
 * @property {Task} depends_on
 */

export {};
