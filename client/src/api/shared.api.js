/**
 * @param {Response} response
 * @returns {Promise<any>}
 */
export async function parseJson(response) {
    if (response.status === 204) {
        return null;
    }

    const contentType = response.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");

    const body = isJson
        ? await response.json().catch(() => null)
        : await response.text();

    if (!response.ok) {
        const isObject = typeof body === "object" && body !== null;

        const errorCode = isObject ? body.error_code || null : null;

        const validationMessage = isObject
            ? getValidationMessage(body.detail)
            : null;

        const message =
            errorCode ||
            validationMessage ||
            (typeof body === "string" ? body : null) ||
            `Request failed (${response.status})`;

        throw new ApiError(message, {
            status: response.status,
            errorCode,
            body,
        });
    }

    return body;
}

/**
 * @typedef {Object} ValidationErrorDetail
 * @property {string} [type]
 * @property {Array<string|number>} [loc]
 * @property {string} [msg]
 * @property {*} [input]
 */

/**
 * @param {ValidationErrorDetail[]|string|undefined|null} detail
 * @returns {string|null}
 */
function getValidationMessage(detail) {
    if (Array.isArray(detail)) {
        return detail
            .map((error) => {
                const location = error.loc?.join(".") || "field";
                return `${location}: ${error.msg || "Invalid value"}`;
            })
            .join(", ");
    }

    if (typeof detail === "string") {
        return detail;
    }

    return null;
}

/**
 * @typedef {Object} ApiErrorOptions
 * @property {number} [status]
 * @property {string|null} [errorCode]
 * @property {*} [body]
 */

export class ApiError extends Error {
    /**
     * @param {string} message
     * @param {ApiErrorOptions} [options={}]
     */
    constructor(message, { status, errorCode = null, body = null } = {}) {
        super(message);

        this.name = "ApiError";
        this.status = status;
        this.errorCode = errorCode;
        this.body = body;

        Object.setPrototypeOf(this, new.target.prototype);
    }
}
