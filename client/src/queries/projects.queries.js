import {
    useInfiniteQuery,
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/vue-query";
import { computed, toValue } from "vue";
import {
    createProject,
    deleteProject,
    getProject,
    getProjectSummary,
    listProjects,
    updateProject,
} from "@/api/projects.api";
import { getSessionGeneration } from "@/queries/client";
import { dashboardKeys } from "@/queries/dashboard.queries";

/**
 * @typedef {import("@/types/project").ProjectCreate} ProjectCreate
 * @typedef {import("@/types/project").ProjectUpdate} ProjectUpdate
 * @typedef {import("@/types/project").ProjectFilterParams} ProjectFilterParams
 */

export const projectKeys = {
    all: ["projects"],
    lists: () => [...projectKeys.all, "list"],
    list: (params = {}) => [...projectKeys.lists(), params],
    details: () => [...projectKeys.all, "detail"],
    detail: (/** @type {number | null | undefined} */ id) => [
        ...projectKeys.details(),
        id,
    ],
    summaries: () => [...projectKeys.all, "summary"],
    summary: (/** @type {number | null | undefined} */ id) => [
        ...projectKeys.summaries(),
        id,
    ],
};

/**
 * @param {import("vue").MaybeRefOrGetter<ProjectFilterParams>} [params]
 */
export function useProjectsList(params = {}, options = {}) {
    const filters = computed(() => toValue(params) ?? {});
    const query = useInfiniteQuery({
        queryKey: computed(() => projectKeys.list(filters.value)),
        queryFn: ({ pageParam, signal }) =>
            listProjects(
                { ...filters.value, cursor: pageParam ?? null },
                signal
            ),
        initialPageParam: /** @type {string | null} */ (null),
        getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
        ...options,
    });

    return {
        ...query,
        items: computed(
            () => query.data.value?.pages.flatMap((page) => page.items) ?? []
        ),
        nextCursor: computed(
            () => query.data.value?.pages.at(-1)?.next_cursor ?? null
        ),
    };
}

/**
 * @param {import("vue").MaybeRefOrGetter<number | null | undefined>} id
 */
export function useProject(id, options = {}) {
    const projectId = computed(() => toValue(id));
    return useQuery({
        queryKey: computed(() => projectKeys.detail(projectId.value)),
        queryFn: ({ signal }) =>
            getProject(/** @type {number} */ (projectId.value), signal),
        enabled: computed(() => projectId.value != null),
        ...options,
    });
}

/**
 * @param {import("vue").MaybeRefOrGetter<number | null | undefined>} id
 */
export function useProjectSummary(id, options = {}) {
    const projectId = computed(() => toValue(id));
    return useQuery({
        queryKey: computed(() => projectKeys.summary(projectId.value)),
        queryFn: ({ signal }) =>
            getProjectSummary(/** @type {number} */ (projectId.value), signal),
        enabled: computed(() => projectId.value != null),
        ...options,
    });
}

export function useCreateProject() {
    const queryClient = useQueryClient();
    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {ProjectCreate} payload
         */
        mutationFn: (payload) => createProject(payload),
        onSuccess: (project, _payload, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.setQueryData(
                projectKeys.detail(project.public_id),
                project
            );
            queryClient.invalidateQueries({ queryKey: projectKeys.lists() });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}

export function useUpdateProject() {
    const queryClient = useQueryClient();
    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ id: number, payload: ProjectUpdate }} vars
         */
        mutationFn: ({ id, payload }) => updateProject(id, payload),
        onSuccess: (project, _vars, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.setQueryData(
                projectKeys.detail(project.public_id),
                project
            );
            queryClient.invalidateQueries({ queryKey: projectKeys.lists() });
            queryClient.invalidateQueries({
                queryKey: projectKeys.summary(project.public_id),
            });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}

export function useDeleteProject() {
    const queryClient = useQueryClient();
    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {number} id
         */
        mutationFn: (id) => deleteProject(id),
        onSuccess: (_data, id, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.removeQueries({ queryKey: projectKeys.detail(id) });
            queryClient.removeQueries({ queryKey: projectKeys.summary(id) });
            queryClient.invalidateQueries({ queryKey: projectKeys.lists() });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}
