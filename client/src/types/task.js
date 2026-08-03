/**
 * @typedef {'open' | 'in_progress' | 'done'} TaskStatus
 */

/**
 * @typedef {'low' | 'medium' | 'high'} TaskPriority
 */

/**
 * @typedef {'task' | 'subtask' | 'epic' | 'bug'} TaskType
 */

/**
 *
 @typedef {'blocks' | 'blocked_by' | 'relates_to'} DependencyType
 */

/**
 * @typedef {import("@/api/projects.api").ProjectRead} ProjectRead
 */

/**
 * @typedef {Object} TaskRead
 * @property {string} id UUID
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus} status
 * @property {TaskPriority} priority
 * @property {TaskType} type
 * @property {string} tags
 * @property {string | null} project_id UUID
 * @property {string | null} parent_id UUID
 * @property {string | null} start_date ISO datetime
 * @property {string | null} due_date ISO datetime
 * @property {number | null} estimated_duration_minutes
 * @property {string} created_at ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {ProjectRead} project
 */

/**
 * @typedef {Object} TaskCreate
 * @property {string} title
 * @property {string} [description]
 * @property {TaskStatus} [status]
 * @property {TaskPriority} [priority]
 * @property {TaskType} [type]
 * @property {string} [tags]
 * @property {string | null} [project_id]
 * @property {string | null} [parent_id]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [due_date] ISO datetime
 * @property {number | null} [estimated_duration_minutes]
 */

/**
 * @typedef {Object} TaskUpdate
 * @property {string} [title]
 * @property {string | null} [description]
 * @property {TaskStatus} [status]
 * @property {TaskPriority} [priority]
 * @property {TaskType} [type]
 * @property {string} [tags]
 * @property {string | null} [project_id]
 * @property {string | null} [parent_id]
 * @property {string | null} [start_date]
 * @property {string | null} [due_date]
 * @property {number | null} [estimated_duration_minutes]
 */

/**
 * @typedef {Object} TaskListResponse
 * @property {TaskRead[]} items
 * @property {string | null} next_cursor
 */

/**
 * @typedef {Object} TaskListParams
 * @property {string} [project_id]
 * @property {TaskStatus} [status]
 * @property {TaskPriority} [priority]
 * @property {TaskType} [type]
 * @property {string} [tag]
 * @property {string} [parent_id]
 * @property {string} [due_before]
 * @property {string} [due_after]
 * @property {?string} [cursor]
 * @property {number} [limit]
 */

/**
 * @typedef {Object} TaskDependencyRead
 * @property {string} id UUID
 * @property {string} task_id UUID
 * @property {string} depends_on_id UUID
 * @property {DependencyType} dependency_type
 */

/**
 * @typedef {Object} TaskDependencyCreate
 * @property {string} task_id UUID
 * @property {string} depends_on_id UUID
 * @property {DependencyType} [dependency_type]
 */

export {};
