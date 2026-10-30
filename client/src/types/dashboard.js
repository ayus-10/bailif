/**
 * @typedef {import("@/types/task").TaskStatus} TaskStatus
 * @typedef {import("@/types/task").TaskPriority} TaskPriority
 * @typedef {import("@/types/taskboards").TaskboardListRead} TaskboardListRead
 */

/**
 * @typedef {Object} DashboardMetric
 * @property {string} key
 * @property {string} label
 * @property {number} value
 * @property {string} icon
 * @property {string} [caption]
 * @property {boolean} [isAlert]
 */

/**
 * @typedef {Object} DashboardProjectStats
 * @property {number} total
 * @property {number} active
 */

/**
 * @typedef {Object} DashboardTaskStats
 * @property {number} total
 * @property {number} completed
 * @property {number} pending
 * @property {number} overdue
 * @property {Partial<Record<TaskStatus, number>>} by_status
 */

/**
 * @typedef {Object} DashboardTaskRead
 * @property {number} public_id
 * @property {string} title
 * @property {TaskStatus} status
 * @property {TaskPriority} priority
 * @property {string | null} due_date ISO datetime
 * @property {string} updated_at ISO datetime
 * @property {number} project_public_id
 * @property {string} project_name
 */

/**
 * @typedef {Object} Dashboard
 * @property {DashboardProjectStats} projects
 * @property {DashboardTaskStats} tasks
 * @property {DashboardTaskRead[]} upcoming_deadlines
 * @property {DashboardTaskRead[]} recent_activity
 * @property {TaskboardListRead[]} taskboards
 */

export {};
