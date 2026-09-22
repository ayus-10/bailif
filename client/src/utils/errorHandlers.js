import { ApiError } from "@/api/shared.api";

/**
 * @param {unknown} err
 * @param {{ error: (message: string) => void }} toast
 */
export function showApiError(err, toast) {
    if (err instanceof ApiError) {
        toast.error(err.message);
    } else {
        toast.error("Something went wrong.");
    }
}
