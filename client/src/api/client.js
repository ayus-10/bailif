import { getSessionGeneration } from "@/queries/client";
import { useAuthStore } from "@/stores/auth";

const BASE_URL = "/api/v1";

/**
 * @type {{ generation: number, promise: Promise<string | null> } | null}
 */
let refreshPromise = null;

/**
 * @returns {Promise<string | null>}
 */
async function performRefresh(sessionGeneration) {
    const authStore = useAuthStore();

    const res = await fetch(`${BASE_URL}/auth/refresh`, {
        method: "POST",
        credentials: "include",
    });

    if (sessionGeneration !== getSessionGeneration()) return null;

    if (!res.ok) {
        await authStore.clearSession();
        return null;
    }

    const data = await res.json();
    if (sessionGeneration !== getSessionGeneration()) return null;

    authStore.setAccessToken(data.token);
    return data.token;
}

/**
 * @returns {Promise<string | null>}
 */
function refreshAccessToken(sessionGeneration) {
    if (refreshPromise?.generation === sessionGeneration) {
        return refreshPromise.promise;
    }

    const promise = performRefresh(sessionGeneration).finally(() => {
        if (refreshPromise?.promise === promise) {
            refreshPromise = null;
        }
    });
    refreshPromise = { generation: sessionGeneration, promise };
    return promise;
}

/**
 * @typedef {Object} ApiFetchOptions
 * @property {boolean} [skipAuth]
 * @property {boolean} [_isRetry]
 */

/**
 * @param {string} path
 * @param {RequestInit & ApiFetchOptions} [options={}]
 * @returns {Promise<Response>}
 */
export async function apiFetch(path, options = {}) {
    const requestSessionGeneration = getSessionGeneration();
    const authStore = useAuthStore();
    const { skipAuth, _isRetry, headers, ...rest } = options;

    const finalHeaders = new Headers(headers);

    if (!skipAuth && authStore.accessToken) {
        finalHeaders.set("Authorization", `Bearer ${authStore.accessToken}`);
    }

    const res = await fetch(`${BASE_URL}${path}`, {
        ...rest,
        headers: finalHeaders,
        credentials: "include",
    });

    if (
        res.status === 401 &&
        !skipAuth &&
        !_isRetry &&
        requestSessionGeneration === getSessionGeneration()
    ) {
        const body = await res
            .clone()
            .json()
            .catch(() => null);

        if (requestSessionGeneration !== getSessionGeneration()) return res;

        if (body?.error_code === "access_token_expired") {
            const newToken = await refreshAccessToken(requestSessionGeneration);

            if (
                newToken &&
                requestSessionGeneration === getSessionGeneration()
            ) {
                return apiFetch(path, {
                    ...options,
                    _isRetry: true,
                });
            }
        }

        if (requestSessionGeneration === getSessionGeneration()) {
            await authStore.clearSession();
        }
    }

    return res;
}
