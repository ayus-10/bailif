import { useAuthStore } from "@/stores/auth";

const BASE_URL = "/api";

/** @type {Promise<string | null> | null} */
let refreshPromise = null;

/** @returns {Promise<string | null>} */
async function performRefresh() {
    const authStore = useAuthStore();

    const res = await fetch(`${BASE_URL}/auth/refresh`, {
        method: "POST",
        credentials: "include",
    });

    if (!res.ok) {
        authStore.clearSession();
        return null;
    }

    const data = await res.json();
    authStore.setAccessToken(data.token);
    return data.token;
}

/** @returns {Promise<string | null>} */
function refreshAccessToken() {
    if (!refreshPromise) {
        refreshPromise = performRefresh().finally(() => {
            refreshPromise = null;
        });
    }

    return refreshPromise;
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

    if (res.status === 401 && !skipAuth && !_isRetry) {
        const body = await res
            .clone()
            .json()
            .catch(() => null);

        // TODO: ensure this remains in sync with server, or find a better way
        if (body?.error_code === "access_token_expired") {
            const newToken = await refreshAccessToken();

            if (newToken) {
                return apiFetch(path, {
                    ...options,
                    _isRetry: true,
                });
            }
        }

        // refresh itself failed, no point retrying
        authStore.clearSession();
    }

    return res;
}
