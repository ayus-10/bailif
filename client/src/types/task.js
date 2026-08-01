/**
 * @typedef {'low' | 'medium' | 'high'} TaskPriority
 */

/**
 * @typedef {'todo' | 'in-progress' | 'done'} TaskStatus
 */

/**
 * @typedef {Object} Task
 * @property {number} id
 * @property {string} title
 * @property {string} project
 * @property {string} due
 * @property {TaskPriority} priority
 * @property {TaskStatus} status
 */

export {};
