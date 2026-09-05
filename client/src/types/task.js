/** @typedef {import("@/types/shared").FetchStatus} FetchStatus */

/**
 * @typedef {'open' | 'in_progress' | 'in_review' | 'done' | 'blocked' | 'cancelled'} TaskStatus
 */

/**
 * @typedef {'low' | 'medium' | 'high'} TaskPriority
 */

/**
 * @typedef {'task' | 'subtask' | 'epic' | 'bug'} TaskType
 */

/**
 * @typedef {'blocks' | 'blocked_by' | 'relates_to'} DependencyType
 */

/**
 * @typedef {"root-tasks" | "child-tasks"} TaskQueryMode
 */

/**
 * @typedef {import("@/api/projects.api").ProjectRead} ProjectRead
 */

/**
 * @typedef {Object} TaskRead
 * @property {string} id
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus} status
 * @property {TaskPriority} priority
 * @property {TaskType} type
 * @property {string} tags
 * @property {string} project_id
 * @property {string | null} parent_id
 * @property {string | null} start_date ISO datetime
 * @property {string | null} due_date ISO datetime
 * @property {string} created_at ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {ProjectRead | null} [project]
 */

/**
 * @typedef {Object} TaskCreate
 * @property {string} title
 * @property {string} project_id
 * @property {string} [description]
 * @property {TaskStatus} [status]
 * @property {TaskPriority} [priority]
 * @property {TaskType} [type]
 * @property {string} [tags]
 * @property {string | null} [parent_id]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [due_date] ISO datetime
 */

/**
 * @typedef {Object} TaskUpdate
 * @property {string} [title]
 * @property {string | null} [description]
 * @property {TaskStatus | null} [status]
 * @property {TaskPriority | null} [priority]
 * @property {TaskType | null} [type]
 * @property {string | null} [tags]
 * @property {string | null} [parent_id]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [due_date] ISO datetime
 */

/**
 * @typedef {Object} TaskListResponse
 * @property {TaskRead[]} items
 * @property {string | null} next_cursor
 */

/**
 * @typedef {Object} TaskListParams
 * @property {string} project_id
 * @property {TaskStatus | null} [status]
 * @property {TaskPriority | null} [priority]
 * @property {TaskType | null} [type]
 * @property {string | null} [tag]
 * @property {string | null} [parent_id]
 * @property {boolean} [only_root]
 * @property {string | null} [due_before] ISO datetime
 * @property {string | null} [due_after] ISO datetime
 * @property {string | null} [cursor]
 * @property {number} [limit]
 */

/**
 * @typedef {Object} TaskDependencyRead
 * @property {string} id
 * @property {string} task_id
 * @property {string} depends_on_id
 * @property {DependencyType} dependency_type
 */

/**
 * @typedef {Object} TaskDependencyCreate
 * @property {string} depends_on_id
 * @property {DependencyType} dependency_type
 */

/**
 * @typedef {Object} TaskDraft
 * @property {string | null} project_id
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus | null} status
 * @property {TaskPriority | null} priority
 * @property {string | null} start_date
 * @property {string | null} due_date
 */

/**
 * @typedef {Object} TaskFetchOptions
 * @property {TaskQueryMode} [queryMode="root-tasks"]
 * @property {string | null} [parentId]
 * @property {string | null} [taskboardId]
 * @property {import("@/types/task").TaskStatus | null} [status]
 * @property {import("@/types/task").TaskPriority | null} [priority]
 * @property {import("@/types/task").TaskType | null} [type]
 * @property {string | null} [tag]
 * @property {string | null} [dueBefore]
 * @property {string | null} [dueAfter]
 * @property {string | null} [cursor]
 * @property {boolean} [append=false]
 * @property {boolean} [forceRefresh=false]
 */

/**
 * @typedef {Object} TasksState
 * @property {Record<string, TaskRead[]>} items
 * @property {Record<string, string | null>} nextCursor
 * @property {Record<string, TaskFetchOptions>} queries
 * @property {TaskRead | null} currentTask
 * @property {Record<string, FetchStatus>} status
 * @property {Record<string, any>} errors
 */

export {};
