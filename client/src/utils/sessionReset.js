import { getActivePinia } from "pinia";
import { advanceSessionGeneration, queryClient } from "@/queries/client";
import { clearRequestCache } from "@/stores/cache";

const AUTH_STORE_ID = "auth";

export async function resetSessionData() {
    advanceSessionGeneration();
    clearRequestCache();
    await queryClient.cancelQueries();
    queryClient.clear();

    const pinia = getActivePinia();

    if (!pinia) return;

    for (const store of pinia._s.values()) {
        if (store.$id !== AUTH_STORE_ID && typeof store.$reset === "function") {
            store.$reset();
        }
    }
}
