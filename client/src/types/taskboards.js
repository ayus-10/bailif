/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 */

/**
 * @typedef {Object} TaskboardForm
 * @property {string} name
 * @property {string} description
 * @property {string} color
 */

/**
 * @typedef {TaskboardForm & { project_public_id: number }} TaskboardPayload
 */

/**
 * @typedef {Object} TaskboardCreate
 * @property {string} name
 * @property {string} [description]
 * @property {string | null} [color] Hex color string
 */

/**
 * @typedef {Object} TaskboardUpdate
 * @property {string | null} [name]
 * @property {string | null} [description]
 * @property {string | null} [color] Hex color string
 */

/**
 * @typedef {Object} TaskboardTaskRead
 * @property {number} position
 * @property {TaskRead | null} [task]
 */

/**
 * @typedef {Object} TaskboardRead
 * @property {number} public_id
 * @property {string} name
 * @property {string} description
 * @property {string | null} color
 * @property {number} project_public_id
 * @property {string} created_at ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {TaskboardTaskRead[]} [tasks]
 */

/**
 * @typedef {Object} TaskboardListRead
 * @property {number} public_id
 * @property {string} name
 * @property {string} description
 * @property {string | null} color
 * @property {number} project_public_id
 * @property {number} task_count
 */

/**
 * @typedef {Object} TaskAssignment
 * @property {number} task_public_id
 * @property {number | null} [position]
 */

/**
 * @typedef {Object} TaskReposition
 * @property {number} position
 */

/**
 * @typedef {Object} TaskboardListResponse
 * @property {TaskboardListRead[]} items
 */

export {};
