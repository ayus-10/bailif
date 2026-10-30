import { QueryCache, QueryClient } from "@tanstack/vue-query";
import { ApiError as ApiErrorClass } from "@/api/shared.api";
import { toast } from "@/composables/useToast";
import { showApiError } from "@/utils/errorHandlers";

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
    queryCache: new QueryCache({
        onError: (error, query) => {
            if (error instanceof ApiErrorClass && error.status === 401) return;

            const meta =
                /** @type {{ sessionGeneration?: number } | undefined} */ (
                    query.meta
                );
            if (meta?.sessionGeneration !== getSessionGeneration()) return;

            showApiError(error, toast);
        },
    }),
    defaultOptions: {
        queries: {
            staleTime: 30_000,
            refetchOnWindowFocus: false,
            refetchOnReconnect: false,
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
