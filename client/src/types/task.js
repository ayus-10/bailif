/**
 * @typedef {import("@/types/shared").RequestStatus} RequestStatus
 */

/**
 * @typedef {"open" | "in_progress" | "in_review" | "done" | "blocked" | "cancelled"} TaskStatus
 */

/**
 * @typedef {"low" | "medium" | "high"} TaskPriority
 */

/**
 * @typedef {"task" | "subtask" | "epic" | "bug"} TaskType
 */

/**
 * @typedef {"root-tasks" | "child-tasks"} TaskQueryMode
 */

/**
 * @typedef {import("@/types/project").ProjectRead} ProjectRead
 */

/**
 * @typedef {Object} TaskRead
 * @property {number} public_id
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus} status
 * @property {TaskPriority} priority
 * @property {TaskType} type
 * @property {string} tags
 * @property {number} project_public_id
 * @property {number | null} parent_public_id
 * @property {string | null} start_date ISO datetime
 * @property {string | null} due_date ISO datetime
 * @property {string} created_at ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {ProjectRead | null} [project]
 */

/**
 * @typedef {TaskRead & {position: number}} TaskWithPosition
 */

/**
 * @typedef {Object} TaskCreate
 * @property {string} title
 * @property {string} [description]
 * @property {TaskStatus} [status]
 * @property {TaskPriority} [priority]
 * @property {TaskType} [type]
 * @property {string} [tags]
 * @property {number | null} [parent_public_id]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [due_date] ISO datetime
 */

/**
 * @typedef {Object} TaskUpdate
 * @property {string | null} [title]
 * @property {string | null} [description]
 * @property {TaskStatus | null} [status]
 * @property {TaskPriority | null} [priority]
 * @property {TaskType | null} [type]
 * @property {string | null} [tags]
 * @property {number | null} [parent_public_id]
 * @property {string | null} [start_date] ISO datetime
 * @property {string | null} [due_date] ISO datetime
 */

/**
 * @typedef {Object} TaskListResponse
 * @property {TaskRead[]} items
 * @property {string | null} [next_cursor]
 */

/**
 * @typedef {Object} TaskListParams
 * @property {TaskStatus | null} [status]
 * @property {TaskPriority | null} [priority]
 * @property {TaskType | null} [type]
 * @property {string | null} [tag]
 * @property {number | null} [parent_public_id]
 * @property {number | null} [taskboard_public_id]
 * @property {boolean} [only_root]
 * @property {string | null} [due_before] ISO datetime
 * @property {string | null} [due_after] ISO datetime
 * @property {string | null} [cursor]
 * @property {number} [limit]
 */

/**
 * @typedef {Object} TaskDraft
 * @property {string} title
 * @property {string} description
 * @property {string} tags
 * @property {TaskStatus | null} status
 * @property {TaskPriority | null} priority
 * @property {string | null} start_date
 * @property {string | null} due_date
 */

/**
 * @typedef {Object} TaskFetchOptions
 * @property {TaskQueryMode} [queryMode="root-tasks"]
 * @property {number | null} [parentId]
 * @property {number | null} [taskboardId]
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
 * @property {Record<string, RequestStatus>} fetchStatus
 * @property {Record<string, any>} fetchErrors
 * @property {Record<string, RequestStatus>} mutationStatus
 * @property {Record<string, any>} mutationErrors
 */

export {};
