import { API_URL } from "@/config";

/**
 * @typedef {Object} RefreshResponse
 * @property {string} accessToken
 */

/** @typedef {RequestInfo | URL} RequestInput */

export class AuthError extends Error {
    constructor(message = "Authentication required") {
        super(message);
        this.name = "AuthError";
    }
}

/** @type {string | null} */
let accessToken = null;

/** @type {Promise<string> | null} */
let refreshPromise = null;

/** @param {string | null} token */
export function setAccessToken(token) {
    accessToken = token;
}

export function clearAccessToken() {
    accessToken = null;
}

export function getAccessToken() {
    return accessToken;
}

export async function initializeAuth() {
    try {
        await refreshAccessToken();
        return true;
    } catch {
        accessToken = null;
        return false;
    }
}

/** @param {string} accessTokenFromServer */
export function handleLogin(accessTokenFromServer) {
    setAccessToken(accessTokenFromServer);
}

export async function logout() {
    try {
        await fetch(`${API_URL}/auth/logout`, {
            method: "POST",
            credentials: "include",
            headers: {
                Accept: "application/json",
            },
        });
    } finally {
        clearAccessToken();
    }
}

/**
 * @param {RequestInput} input
 * @param {RequestInit} [init={}]
 * @returns {Promise<Response>}
 * @throws {AuthError}
 */
export async function apiFetch(input, init = {}) {
    const request = createRequest(input, init);
    let response = await fetch(request);

    if (response.status !== 401) {
        return response;
    }

    let newToken;
    try {
        newToken = await refreshAccessToken();
    } catch {
        accessToken = null;
        throw new AuthError("Your session has expired");
    }

    const retryRequest = createRequest(input, {
        ...init,
        headers: {
            ...headersToObject(init.headers),
            Authorization: `Bearer ${newToken}`,
        },
    });

    return fetch(retryRequest);
}

/**
 * @returns {Promise<string>}
 * @throws {AuthError}
 */
async function refreshAccessToken() {
    if (refreshPromise) {
        return refreshPromise;
    }

    refreshPromise = (async () => {
        try {
            const response = await fetch(`${API_URL}/auth/refresh`, {
                method: "POST",
                credentials: "include",
                headers: {
                    Accept: "application/json",
                },
            });

            if (!response.ok) {
                accessToken = null;
                throw new AuthError("Unable to refresh authentication session");
            }

            const data = await response.json();

            if (!data.accessToken || typeof data.accessToken !== "string") {
                accessToken = null;
                throw new AuthError(
                    "Refresh endpoint returned an invalid access token"
                );
            }

            accessToken = data.accessToken;
            return data.accessToken;
        } finally {
            refreshPromise = null;
        }
    })();

    return refreshPromise;
}

/**
 * @param {RequestInput} input
 * @param {RequestInit} init
 * @returns {Request}
 */
function createRequest(input, init) {
    const headers = new Headers(init.headers);

    if (accessToken && !headers.has("Authorization")) {
        headers.set("Authorization", `Bearer ${accessToken}`);
    }

    return new Request(input, {
        ...init,
        headers,
    });
}

/** @param {HeadersInit} [headers] */
function headersToObject(headers) {
    /** @type {Record<string, string>} */
    const result = {};

    if (!headers) {
        return result;
    }

    const normalized = new Headers(headers);
    normalized.forEach((value, key) => {
        result[key] = value;
    });

    return result;
}
