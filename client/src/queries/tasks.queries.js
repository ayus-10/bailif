import {
    useInfiniteQuery,
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/vue-query";
import { computed, toValue } from "vue";
import {
    createTask,
    deleteTask,
    getTask,
    listTasks,
    updateTask,
} from "@/api/tasks.api";
import { getSessionGeneration } from "@/queries/client";
import { dashboardKeys } from "@/queries/dashboard.queries";
import { projectKeys } from "@/queries/projects.queries";
import { taskboardKeys } from "@/queries/taskboards.queries";

/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 * @typedef {import("@/types/task").TaskCreate} TaskCreate
 * @typedef {import("@/types/task").TaskUpdate} TaskUpdate
 * @typedef {import("@/types/task").TaskFetchOptions} TaskFetchOptions
 * @typedef {import("vue").MaybeRefOrGetter<number | null | undefined>} MaybeId
 * @typedef {import("vue").MaybeRefOrGetter<TaskFetchOptions>} MaybeTaskFilters
 */

/**
 * @param {TaskFetchOptions} [filters]
 * @returns {TaskFetchOptions}
 */
function normalizeTaskFilters(filters = {}) {
    const parentId = filters.parentId ?? null;

    return {
        queryMode:
            filters.queryMode ??
            (parentId == null ? "root-tasks" : "child-tasks"),
        parentId,
        taskboardId: filters.taskboardId ?? null,
        status: filters.status ?? null,
        priority: filters.priority ?? null,
        type: filters.type ?? null,
        tag: filters.tag ?? null,
        dueBefore: filters.dueBefore ?? null,
        dueAfter: filters.dueAfter ?? null,
    };
}

/**
 * @param {TaskFetchOptions} filters
 * @param {string | null} cursor
 */
function toTaskListParams(filters, cursor) {
    const {
        queryMode,
        parentId,
        taskboardId,
        status,
        priority,
        type,
        tag,
        dueBefore,
        dueAfter,
    } = normalizeTaskFilters(filters);

    if (queryMode === "child-tasks" && parentId == null) {
        throw new Error("parentId is required when queryMode is 'child-tasks'");
    }

    return {
        cursor,
        ...(queryMode === "child-tasks"
            ? { parent_public_id: parentId }
            : { only_root: true }),
        ...(taskboardId != null ? { taskboard_public_id: taskboardId } : {}),
        ...(status != null ? { status } : {}),
        ...(priority != null ? { priority } : {}),
        ...(type != null ? { type } : {}),
        ...(tag != null ? { tag } : {}),
        ...(dueBefore != null ? { due_before: dueBefore } : {}),
        ...(dueAfter != null ? { due_after: dueAfter } : {}),
    };
}

export const taskKeys = {
    all: ["tasks"],
    lists: () => [...taskKeys.all, "list"],
    projectLists: (
        /** @type {number | null | undefined} */ projectPublicId
    ) => [...taskKeys.lists(), projectPublicId],
    list: (
        /** @type {number | null | undefined} */ projectPublicId,
        /** @type {TaskFetchOptions} */ filters = {}
    ) => [
        ...taskKeys.projectLists(projectPublicId),
        normalizeTaskFilters(filters),
    ],
    details: () => [...taskKeys.all, "detail"],
    detail: (/** @type {number | null | undefined} */ taskPublicId) => [
        ...taskKeys.details(),
        taskPublicId,
    ],
};

/**
 * @param {MaybeId} projectPublicId
 * @param {MaybeTaskFilters} [filters]
 * @param {Object} [options]
 */
export function useTasksList(projectPublicId, filters = {}, options = {}) {
    const projectId = computed(() => toValue(projectPublicId));
    const normalizedFilters = computed(() =>
        normalizeTaskFilters(toValue(filters) ?? {})
    );
    const query = useInfiniteQuery({
        queryKey: computed(() =>
            taskKeys.list(projectId.value, normalizedFilters.value)
        ),
        queryFn: ({ pageParam, signal }) =>
            listTasks(
                toTaskListParams(
                    normalizedFilters.value,

                    /** @type {string | null} */ (pageParam ?? null)
                ),
                signal
            ),
        initialPageParam: /** @type {string | null} */ (null),
        getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
        enabled: computed(() => projectId.value != null),
        ...options,
        meta: { sessionGeneration: getSessionGeneration() },
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
 * @param {MaybeId} taskPublicId
 * @param {Object} [options]
 */
export function useTask(taskPublicId, options = {}) {
    const id = computed(() => toValue(taskPublicId));

    return useQuery({
        queryKey: computed(() => taskKeys.detail(id.value)),
        queryFn: ({ signal }) =>
            getTask(/** @type {number} */ (id.value), signal),
        enabled: computed(() => id.value != null),
        ...options,
        meta: { sessionGeneration: getSessionGeneration() },
    });
}

/**
 * @param {import("@tanstack/vue-query").QueryClient} queryClient
 * @param {number | null | undefined} projectPublicId
 */
function invalidateTaskAggregates(queryClient, projectPublicId) {
    void queryClient.invalidateQueries({ queryKey: dashboardKeys.all });

    if (projectPublicId == null) {
        void queryClient.invalidateQueries({ queryKey: taskboardKeys.lists() });
        void queryClient.invalidateQueries({
            queryKey: projectKeys.summaries(),
        });
        return;
    }

    void queryClient.invalidateQueries({
        queryKey: taskboardKeys.list(projectPublicId),
    });
    void queryClient.invalidateQueries({
        queryKey: projectKeys.summary(projectPublicId),
    });
}

export function useCreateTask() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {TaskCreate} payload
         */
        mutationFn: (payload) => createTask(payload),
        onSuccess: (task, _payload, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;

            queryClient.setQueryData(taskKeys.detail(task.public_id), task);
            void queryClient.invalidateQueries({
                queryKey: taskKeys.projectLists(task.project_public_id),
            });
            invalidateTaskAggregates(queryClient, task.project_public_id);
        },
    });
}

export function useUpdateTask() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ taskPublicId: number, payload: TaskUpdate }} variables
         */
        mutationFn: ({ taskPublicId, payload }) =>
            updateTask(taskPublicId, payload),
        onSuccess: (task, _variables, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;

            queryClient.setQueryData(taskKeys.detail(task.public_id), task);
            void queryClient.invalidateQueries({
                queryKey: taskKeys.projectLists(task.project_public_id),
            });
            invalidateTaskAggregates(queryClient, task.project_public_id);
        },
    });
}

export function useDeleteTask() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ taskPublicId: number, projectPublicId?: number }} variables
         */
        mutationFn: ({ taskPublicId }) => deleteTask(taskPublicId),
        onSuccess: (
            _data,
            { taskPublicId, projectPublicId },
            mutationSessionGeneration
        ) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;

            queryClient.removeQueries({
                queryKey: taskKeys.detail(taskPublicId),
            });
            void queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? taskKeys.lists()
                        : taskKeys.projectLists(projectPublicId),
            });
            invalidateTaskAggregates(queryClient, projectPublicId);
        },
    });
}
