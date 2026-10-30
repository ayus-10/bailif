import { QueryClient } from "@tanstack/vue-query";

/**
 * @typedef {import("@/api/shared.api").ApiError} ApiError
 */

let sessionGeneration = 0;

export function getSessionGeneration() {
    return sessionGeneration;
}

export function advanceSessionGeneration() {
    sessionGeneration += 1;
    return sessionGeneration;
}

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 30_000,
            retry: (failureCount, error) => {
                /**
                 * @type {ApiError}
                 */
                const apiError = /** @type {ApiError} */ (
                    /** @type {unknown} */ (error)
                );
                const status = apiError.status ?? 0;
                return status >= 400 && status < 500 ? false : failureCount < 2;
            },
        },
    },
});

/**
 * Clear cached server state when the authenticated account changes.
 */
export function clearQueryCache() {
    advanceSessionGeneration();
    queryClient.clear();
}
