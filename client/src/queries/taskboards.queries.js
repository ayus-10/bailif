import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { computed, toValue } from "vue";
import {
    addTaskToBoard,
    createTaskboard,
    deleteTaskboard,
    getTaskboard,
    listTaskboards,
    removeTaskFromBoard,
    repositionTask,
    updateTaskboard,
} from "@/api/taskboards.api";
import { getSessionGeneration } from "@/queries/client";
import { dashboardKeys } from "@/queries/dashboard.queries";
import { projectKeys } from "@/queries/projects.queries";

/**
 * @typedef {import("@/api/shared.api").ApiError} ApiError
 * @typedef {import("@/types/taskboards").TaskboardRead} TaskboardRead
 * @typedef {import("@/types/taskboards").TaskboardListRead} TaskboardListRead
 * @typedef {import("@/types/taskboards").TaskboardCreate} TaskboardCreate
 * @typedef {import("@/types/taskboards").TaskboardUpdate} TaskboardUpdate
 * @typedef {import("@/types/taskboards").TaskboardPayload} TaskboardPayload
 * @typedef {import("@/types/taskboards").TaskAssignment} TaskAssignment
 * @typedef {import("@/types/taskboards").TaskReposition} TaskReposition
 * @typedef {import("@/types/taskboards").TaskboardTaskRead} TaskboardTaskRead

 * @typedef {import("vue").MaybeRefOrGetter<number | null | undefined>} MaybeId
 */

export const taskboardKeys = {
    all: ["taskboards"],
    lists: () => [...taskboardKeys.all, "list"],
    list: (/** @type {number | null | undefined} */ projectPublicId) => [
        ...taskboardKeys.lists(),
        projectPublicId,
    ],
    details: () => [...taskboardKeys.all, "detail"],
    detail: (/** @type {number | null | undefined} */ id) => [
        ...taskboardKeys.details(),
        id,
    ],
};

/**
 * @param {MaybeId} projectPublicId
 * @param {Object} [options]
 */
export function useTaskboardsList(projectPublicId, options = {}) {
    const query = useQuery({
        queryKey: computed(() => taskboardKeys.list(toValue(projectPublicId))),
        queryFn: ({ signal }) =>
            listTaskboards(
                /** @type {number} */ (toValue(projectPublicId)),
                signal
            ),
        enabled: computed(() => toValue(projectPublicId) != null),
        ...options,
    });

    const items = computed(() => query.data.value?.items ?? []);

    return {
        ...query,
        items,
    };
}

/**
 * @param {MaybeId} boardPublicId
 * @param {Object} [options]
 */
export function useTaskboard(boardPublicId, options = {}) {
    return useQuery({
        queryKey: computed(() => taskboardKeys.detail(toValue(boardPublicId))),
        queryFn: ({ signal }) =>
            getTaskboard(
                /** @type {number} */ (toValue(boardPublicId)),
                signal
            ),
        enabled: computed(() => toValue(boardPublicId) != null),
        ...options,
    });
}

export function useCreateTaskboard() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {TaskboardPayload} payload
         */
        mutationFn: (payload) => createTaskboard(payload),
        onSuccess: (board, _payload, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.setQueryData(
                taskboardKeys.detail(board.public_id),
                board
            );
            queryClient.invalidateQueries({
                queryKey: taskboardKeys.list(board.project_public_id),
            });
            queryClient.invalidateQueries({
                queryKey: projectKeys.summary(board.project_public_id),
            });
            queryClient.invalidateQueries({
                queryKey: dashboardKeys.all,
            });
        },
    });
}

export function useUpdateTaskboard() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ id: number, payload: TaskboardUpdate }} vars
         */
        mutationFn: ({ id, payload }) => updateTaskboard(id, payload),
        onSuccess: (board, { id }, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.setQueryData(taskboardKeys.detail(id), board);
            queryClient.invalidateQueries({
                queryKey: taskboardKeys.list(board.project_public_id),
            });
            queryClient.invalidateQueries({
                queryKey: projectKeys.summary(board.project_public_id),
            });
            queryClient.invalidateQueries({
                queryKey: dashboardKeys.all,
            });
        },
    });
}

export function useDeleteTaskboard() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {number | { id: number, projectPublicId?: number }} idOrVars
         */
        mutationFn: (idOrVars) => {
            const id = typeof idOrVars === "number" ? idOrVars : idOrVars.id;
            return deleteTaskboard(id);
        },
        onSuccess: (_data, idOrVars, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            const id = typeof idOrVars === "number" ? idOrVars : idOrVars.id;
            const cachedBoard = /** @type {TaskboardRead | undefined} */ (
                queryClient.getQueryData(taskboardKeys.detail(id))
            );
            const projectPublicId =
                typeof idOrVars === "number"
                    ? cachedBoard?.project_public_id
                    : (idOrVars.projectPublicId ??
                      cachedBoard?.project_public_id);

            queryClient.removeQueries({ queryKey: taskboardKeys.detail(id) });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? taskboardKeys.lists()
                        : taskboardKeys.list(projectPublicId),
            });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? projectKeys.summaries()
                        : projectKeys.summary(projectPublicId),
            });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}

export function useAddTaskToBoard() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ boardPublicId: number, payload: TaskAssignment }} vars
         */
        mutationFn: ({ boardPublicId, payload }) =>
            addTaskToBoard(boardPublicId, payload),
        onSuccess: (_task, { boardPublicId }, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            const board = /** @type {TaskboardRead | undefined} */ (
                queryClient.getQueryData(taskboardKeys.detail(boardPublicId))
            );
            const projectPublicId = board?.project_public_id;

            queryClient.invalidateQueries({
                queryKey: taskboardKeys.detail(boardPublicId),
            });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? taskboardKeys.lists()
                        : taskboardKeys.list(projectPublicId),
            });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? projectKeys.summaries()
                        : projectKeys.summary(projectPublicId),
            });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}

export function useRemoveTaskFromBoard() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ boardPublicId: number, taskPublicId: number }} vars
         */
        mutationFn: ({ boardPublicId, taskPublicId }) =>
            removeTaskFromBoard(boardPublicId, taskPublicId),
        onSuccess: (_data, { boardPublicId }, mutationSessionGeneration) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            const board = /** @type {TaskboardRead | undefined} */ (
                queryClient.getQueryData(taskboardKeys.detail(boardPublicId))
            );
            const projectPublicId = board?.project_public_id;

            queryClient.invalidateQueries({
                queryKey: taskboardKeys.detail(boardPublicId),
            });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? taskboardKeys.lists()
                        : taskboardKeys.list(projectPublicId),
            });
            queryClient.invalidateQueries({
                queryKey:
                    projectPublicId == null
                        ? projectKeys.summaries()
                        : projectKeys.summary(projectPublicId),
            });
            queryClient.invalidateQueries({ queryKey: dashboardKeys.all });
        },
    });
}

export function useRepositionTask() {
    const queryClient = useQueryClient();

    return useMutation({
        onMutate: () => getSessionGeneration(),

        /**
         * @param {{ boardPublicId: number, taskPublicId: number, payload: TaskReposition }} vars
         */
        mutationFn: ({ boardPublicId, taskPublicId, payload }) =>
            repositionTask(boardPublicId, taskPublicId, payload),
        onSuccess: (
            _data,
            { boardPublicId, taskPublicId, payload },
            mutationSessionGeneration
        ) => {
            if (mutationSessionGeneration !== getSessionGeneration()) return;
            queryClient.setQueryData(
                taskboardKeys.detail(boardPublicId),
                (/** @type {TaskboardRead | undefined} */ board) => {
                    if (!board?.tasks) return board;
                    const tasks = [...board.tasks];
                    const fromIndex = tasks.findIndex(
                        (entry) => entry.task?.public_id === taskPublicId
                    );
                    if (fromIndex !== -1) {
                        const [movedTask] = tasks.splice(fromIndex, 1);
                        tasks.splice(payload.position, 0, movedTask);
                        return {
                            ...board,
                            tasks: tasks.map((entry, index) => ({
                                ...entry,
                                position: index,
                            })),
                        };
                    }
                    return board;
                }
            );
            queryClient.invalidateQueries({
                queryKey: taskboardKeys.detail(boardPublicId),
            });
        },
    });
}
