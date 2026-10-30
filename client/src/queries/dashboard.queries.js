import { useQuery } from "@tanstack/vue-query";
import { fetchDashboard } from "@/api/dashboard.api";
import { getSessionGeneration } from "@/queries/client";

export const dashboardKeys = {
    all: ["dashboard"],
};

export function useDashboard(options = {}) {
    return useQuery({
        queryKey: dashboardKeys.all,
        queryFn: ({ signal }) => fetchDashboard(signal),
        refetchOnMount: "always",
        ...options,
        meta: { sessionGeneration: getSessionGeneration() },
    });
}
