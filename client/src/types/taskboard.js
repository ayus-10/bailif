/** @typedef {import('@/types/task').TaskRead} TaskRead */

/**
 * @typedef {Object} TaskboardCreate
 * @property {string} name
 * @property {string | null} [description]
 * @property {string | null} [color]
 * @property {string | null} [project_id]
 */

/**
 * @typedef {Object} TaskboardUpdate
 * @property {string} [name]
 * @property {string} [description]
 * @property {string | null} [color]
 */

/**
 * @typedef {Object} TaskboardTaskRead
 * @property {string} id
 * @property {string} task_id
 * @property {number} position
 * @property {TaskRead | null} [task]
 */

/**
 * @typedef {Object} TaskboardRead
 * @property {string} id
 * @property {string} name
 * @property {string} description
 * @property {string | null} color
 * @property {string | null} project_id
 * @property {string} created_at
 * @property {string} updated_at
 * @property {TaskboardTaskRead[]} tasks
 */

/**
 * @typedef {Object} TaskboardListRead
 * @property {string} id
 * @property {string} name
 * @property {string} description
 * @property {string | null} color
 * @property {string | null} project_id
 * @property {number} task_count
 */

/**
 * @typedef {Object} TaskAssignment
 * @property {string} task_id
 * @property {number | null} [position]
 */

/**
 * @typedef {Object} TaskReposition
 * @property {string} task_id
 * @property {number} position
 */

/**
 * @typedef {Object} TaskboardListResponse
 * @property {TaskboardListRead[]} items
 */

export {};
