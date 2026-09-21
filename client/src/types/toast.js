/**
 * @typedef {string | number} ToastId
 */

/**
 * @typedef {"default" | "success" | "error" | "warning" | "info"} ToastType
 */

/**
 * @typedef {"top-left" | "top-center" | "top-right" | "bottom-left" | "bottom-center" | "bottom-right"} ToastPosition
 */

/**
 * @typedef {Object} ToastComponentContent
 * @property {import("vue").Component} component
 * @property {Record<string, unknown>} [props]
 */

/**
 * @typedef {string | ToastComponentContent} ToastContent
 */

/**
 * @typedef {Object} ToastOptions
 * @property {ToastId} [id]
 * @property {ToastType} [type]
 * @property {ToastPosition} [position]
 * @property {number | false} [timeout]
 * @property {boolean} [closeOnClick]
 * @property {boolean} [pauseOnHover]
 * @property {boolean} [pauseOnFocusLoss]
 * @property {boolean} [showCloseButton]
 * @property {boolean} [hideProgressBar]
 * @property {boolean | string} [icon]
 * @property {(toast: ToastItem) => void} [onClick]
 * @property {(toast: ToastItem) => void} [onClose]
 */

/**
 * @typedef {Object} ToastItem
 * @property {ToastId} id
 * @property {ToastType} type
 * @property {ToastPosition} position
 * @property {number | false} timeout
 * @property {boolean} closeOnClick
 * @property {boolean} pauseOnHover
 * @property {boolean} pauseOnFocusLoss
 * @property {boolean} showCloseButton
 * @property {boolean} hideProgressBar
 * @property {boolean | string} icon
 * @property {ToastContent} content
 * @property {boolean} paused
 * @property {number} version
 * @property {string | null} iconName
 * @property {boolean} hasComponent
 * @property {(toast: ToastItem) => void} [onClick]
 * @property {(toast: ToastItem) => void} [onClose]
 */

export {};
