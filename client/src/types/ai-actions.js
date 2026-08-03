/**
 * @typedef {'LOW' | 'MEDIUM' | 'HIGH'} AiPriority
 */

/**
 * @typedef {'CREATE_PROJECT'
 *   | 'UPDATE_PROJECT'
 *   | 'ARCHIVE_PROJECT'
 *   | 'DELETE_PROJECT'
 *   | 'CREATE_TASK'
 *   | 'UPDATE_TASK'
 *   | 'DELETE_TASK'
 *   | 'COMPLETE_TASK'
 *   | 'REOPEN_TASK'
 *   | 'SEARCH_TASKS'
 *   | 'SEARCH_PROJECTS'
 *   | 'SUGGEST_TASKS'
 *   | 'RECOMMEND_NEXT_TASK'
 * } ActionType
 */

/**
 * @typedef {Object} ChatRequest
 * @property {string | null} [message]
 * @property {string | null} [project_id]
 *
 * // bypass mode
 * @property {string | null} [title]
 * @property {string | null} [description]
 * @property {string | null} [query]
 * @property {number} [top_k]
 */

/**
 * @typedef {'suggest_tasks' | 'search_tasks'} ChatMode
 */

/**
 * @typedef {Object} CreateProjectData
 * @property {string} name
 * @property {string | null} [description]
 */

/**
 * @typedef {Object} UpdateProjectData
 * @property {string} id
 * @property {string | null} [name]
 * @property {string | null} [description]
 */

/**
 * @typedef {Object} ArchiveProjectData
 * @property {string} id
 */

/**
 * @typedef {Object} DeleteProjectData
 * @property {string} id
 */

/**
 * @typedef {Object} CreateTaskData
 * @property {string} title
 * @property {string | null} [description]
 * @property {AiPriority} [priority]
 * @property {string | null} [project_id]
 */

/**
 * @typedef {Object} UpdateTaskData
 * @property {string} id
 * @property {string | null} [title]
 * @property {string | null} [description]
 * @property {AiPriority | null} [priority]
 */

/**
 * @typedef {Object} DeleteTaskData
 * @property {string} id
 */

/**
 * @typedef {Object} CompleteTaskData
 * @property {string} id
 */

/**
 * @typedef {Object} ReopenTaskData
 * @property {string} id
 */

/**
 * @typedef {Object} SearchTasksData
 * @property {string | null} [query]
 * @property {string | null} [project_id]
 * @property {string | null} [status]
 * @property {AiPriority | null} [priority]
 */

/**
 * @typedef {Object} SearchProjectsData
 * @property {string | null} [query]
 */

/**
 * @typedef {Object} SuggestTasksData
 * @property {string | null} [project_id]
 * @property {number | null} [count]
 */

/**
 * @typedef {Object} RecommendNextTaskData
 * @property {string | null} [project_id]
 */

/**
 * @typedef {Object} CreateProjectAction
 * @property {'create_project'} type
 * @property {CreateProjectData} data
 */

/**
 * @typedef {Object} UpdateProjectAction
 * @property {'update_project'} type
 * @property {UpdateProjectData} data
 */

/**
 * @typedef {Object} ArchiveProjectAction
 * @property {'archive_project'} type
 * @property {ArchiveProjectData} data
 */

/**
 * @typedef {Object} DeleteProjectAction
 * @property {'delete_project'} type
 * @property {DeleteProjectData} data
 */

/**
 * @typedef {Object} CreateTaskAction
 * @property {'create_task'} type
 * @property {CreateTaskData} data
 */

/**
 * @typedef {Object} UpdateTaskAction
 * @property {'update_task'} type
 * @property {UpdateTaskData} data
 */

/**
 * @typedef {Object} DeleteTaskAction
 * @property {'delete_task'} type
 * @property {DeleteTaskData} data
 */

/**
 * @typedef {Object} CompleteTaskAction
 * @property {'complete_task'} type
 * @property {CompleteTaskData} data
 */

/**
 * @typedef {Object} ReopenTaskAction
 * @property {'reopen_task'} type
 * @property {ReopenTaskData} data
 */

/**
 * @typedef {Object} SearchTasksAction
 * @property {'search_tasks'} type
 * @property {SearchTasksData} data
 */

/**
 * @typedef {Object} SearchProjectsAction
 * @property {'search_projects'} type
 * @property {SearchProjectsData} data
 */

/**
 * @typedef {Object} SuggestTasksAction
 * @property {'suggest_tasks'} type
 * @property {SuggestTasksData} data
 */

/**
 * @typedef {Object} RecommendNextTaskAction
 * @property {'recommend_next_task'} type
 * @property {RecommendNextTaskData} data
 */

/**
 * @typedef {CreateProjectAction | UpdateProjectAction | ArchiveProjectAction | DeleteProjectAction | CreateTaskAction | UpdateTaskAction | DeleteTaskAction | CompleteTaskAction | ReopenTaskAction | SearchTasksAction | SearchProjectsAction | SuggestTasksAction | RecommendNextTaskAction} ActionItem
 */

/**
 * @typedef {Object} ChatResponse
 * @property {string | null} action_id
 * @property {string} reply
 * @property {ActionItem[]} actions
 * @property {any} results
 */

export {};
