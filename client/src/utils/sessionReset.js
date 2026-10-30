import { getActivePinia } from "pinia";
import { clearRequestCache } from "@/stores/cache";

const AUTH_STORE_ID = "auth";

export function resetSessionData() {
    const pinia = getActivePinia();

    if (!pinia) return;

    // Pinia keeps every registered store in the internal `_s` map.
    // @ts-ignore
    for (const store of pinia._s.values()) {
        if (store.$id !== AUTH_STORE_ID) store.$reset();
    }

    clearRequestCache();
}
