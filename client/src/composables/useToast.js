import { markRaw, reactive } from "vue";
import { TOAST_ICONS } from "@/constants/toast";

/**
 * @typedef {import("@/types/toast").ToastContent} ToastContent
 * @typedef {import("@/types/toast").ToastOptions} ToastOptions
 * @typedef {import("@/types/toast").ToastItem} ToastItem
 * @typedef {import("@/types/toast").ToastId} ToastId
 * @typedef {import("@/types/toast").ToastPosition} ToastPosition
 * @typedef {import("@/types/toast").ToastComponentContent} ToastComponentContent
 */

const config = reactive({
    position: /** @type {ToastPosition} */ ("top-right"),
    timeout: 5000,
    closeOnClick: true,
    pauseOnHover: true,
    pauseOnFocusLoss: true,
    showCloseButton: true,
    hideProgressBar: false,
    icon: true,
    maxToasts: 5,
    newestOnTop: true,
});
export const toasts = reactive(/** @type {ToastItem[]} */ ([]));

let nextId = 1;

/**
 * @param {ToastContent} content
 * @returns {ToastContent}
 */
function normalizeContent(content) {
    if (content && typeof content === "object" && content.component) {
        return { ...content, component: markRaw(content.component) };
    }
    return content;
}

/**
 * @param {ToastId} id
 */
function dismiss(id) {
    const index = toasts.findIndex((t) => t.id === id);
    if (index === -1) return;
    const [removed] = toasts.splice(index, 1);
    removed.onClose?.(removed);
}

function clear() {
    toasts.splice(0).forEach((t) => t.onClose?.(t));
}

/**
 * @param {ToastId} id
 * @param {{ content?: ToastContent, options?: ToastOptions }} [payload]
 */
function update(id, { content, options } = {}) {
    const target = toasts.find((t) => t.id === id);
    if (!target) return;
    if (content !== undefined) target.content = normalizeContent(content);
    if (options) Object.assign(target, options, { id });
    target.version++;
}

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
function create(content, options = {}) {
    const id = options.id ?? nextId++;

    if (toasts.some((t) => t.id === id)) {
        update(id, { content, options });
        return id;
    }

    const { maxToasts, newestOnTop, ...defaults } = config;

    /**
     * @type {ToastItem}
     */
    const item = {
        /**
         * @type {keyof typeof TOAST_ICONS}
         */
        type: "default",
        ...defaults,
        ...options,

        id,
        content: normalizeContent(content),
        paused: false,
        version: 0,

        /**
         * @returns {string | null}
         */
        get iconName() {
            if (this.icon === false) return null;
            if (typeof this.icon === "string") return this.icon;
            return TOAST_ICONS[this.type] ?? TOAST_ICONS.default;
        },

        /**
         * @returns {boolean}
         */
        get hasComponent() {
            const c = this.content;
            return c !== null && typeof c === "object" && "component" in c;
        },
    };

    if (newestOnTop) toasts.unshift(item);
    else toasts.push(item);

    while (toasts.length > maxToasts) {
        dismiss(newestOnTop ? toasts[toasts.length - 1].id : toasts[0].id);
    }

    return id;
}

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
export const toast = (content, options) => create(content, options);

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
toast.success = (content, options) =>
    create(content, { ...options, type: "success" });

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
toast.error = (content, options) =>
    create(content, { ...options, type: "error" });

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
toast.warning = (content, options) =>
    create(content, { ...options, type: "warning" });

/**
 * @param {ToastContent} content
 * @param {ToastOptions} [options]
 */
toast.info = (content, options) =>
    create(content, { ...options, type: "info" });

toast.update = update;
toast.dismiss = dismiss;
toast.clear = clear;

/**
 * @param {ToastOptions} options
 */
export function setToastDefaults(options) {
    Object.assign(config, options);
}

export function useToast() {
    return toast;
}
