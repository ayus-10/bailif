<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, ref } from "vue";
import ConfirmDialog from "@/components/common/ConfirmDialog.vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import BoardHeader from "@/components/taskboards/BoardHeader.vue";
import BoardToolbar from "@/components/taskboards/BoardToolbar.vue";
import CreateTaskBoardModel from "@/components/taskboards/CreateTaskBoardModel.vue";
import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { STATUS_META } from "@/constants/tasks";
import {
    useDeleteTaskboard,
    useTaskboard,
    useTaskboardsList,
} from "@/queries/taskboards.queries";
import {
    useDeleteTask,
    useTasksList,
    useUpdateTask,
} from "@/queries/tasks.queries";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 * @typedef {import("@/types/task").TaskWithPosition} TaskWithPosition
 * @typedef {import("@/types/task").TaskCreate} TaskCreate
 * @typedef {import("@/types/task").TaskQueryMode} TaskQueryMode
 */

/**
 * @typedef {Object} AllBoardSelection
 * @property {"all"} type
 */

/**
 * @typedef {Object} SingleBoardSelection
 * @property {"single"} type
 * @property {number} id
 */

/**
 * @typedef {AllBoardSelection | SingleBoardSelection} BoardSelection
 */

const toast = useToast();

const route = useRoute();
const router = useRouter();

const { projectId } = useActiveProject();

/**
 * @type {import("vue").ComputedRef<BoardSelection>}
 */
const currentBoard = computed(() => {
    const id = route.params.id;

    if (!id || id === "all") {
        return { type: "all" };
    }

    return {
        type: "single",
        id: Array.isArray(id) ? Number(id[0]) : Number(id),
    };
});

/**
 * @type {import("vue").Ref<TaskQueryMode>}
 */
const preferredQueryMode = ref("root-tasks");

const query = computed(() => ({
    queryMode: preferredQueryMode.value,
    taskboardId:
        currentBoard.value.type === "single" ? currentBoard.value.id : null,
}));

const tasksQuery = useTasksList(projectId, query);
const updateTaskMutation = useUpdateTask();
const deleteTaskMutation = useDeleteTask();

const boardId = computed(() =>
    currentBoard.value.type === "single" ? currentBoard.value.id : null
);
const taskboardQuery = useTaskboard(boardId);
const taskboardsQuery = useTaskboardsList(projectId);
const deleteTaskboardMutation = useDeleteTaskboard();
const taskboard = computed(() => taskboardQuery.data.value ?? null);

const boardSummary = computed(() =>
    currentBoard.value.type === "single"
        ? (taskboardsQuery.items.value.find(
              (item) =>
                  item.public_id ===
                  /** @type {SingleBoardSelection} */ (currentBoard.value).id
          ) ?? null)
        : null
);

const tasks = tasksQuery.items;
const isLoading = computed(
    () => tasksQuery.isLoading.value && tasks.value.length === 0
);
const hasError = computed(
    () => tasksQuery.isError.value && tasks.value.length === 0
);
const hasNextPage = tasksQuery.hasNextPage;
const isFetchingNextPage = tasksQuery.isFetchingNextPage;

const searchText = ref("");

const statusFilter = computed(() =>
    typeof route.query.status === "string" ? route.query.status : null
);

const priorityFilter = computed(() =>
    typeof route.query.priority === "string" ? route.query.priority : null
);

const filteredTasks = computed(() => {
    const search = searchText.value.trim().toLowerCase();

    return tasks.value.filter((task) => {
        if (statusFilter.value && task.status !== statusFilter.value) {
            return false;
        }

        if (priorityFilter.value && task.priority !== priorityFilter.value) {
            return false;
        }

        return !search || task.title.toLowerCase().includes(search);
    });
});

const tasksByStatus = computed(() => {
    return filteredTasks.value.reduce((acc, task, idx) => {
        if (!acc[task.status]) {
            acc[task.status] = [];
        }

        acc[task.status].push({ ...task, position: idx });

        return acc;
    }, /** @type {Record<string, TaskWithPosition[]>} */ ({}));
});

const draggedTask = ref(/** @type {TaskWithPosition | null} */ (null));

/**
 * @type {import("vue").Ref<TaskCreate | null>}
 */
const pendingTask = ref(null);

const showEditBoard = ref(false);
const showDeleteBoard = ref(false);
const taskToDelete = ref(/** @type {TaskRead | null} */ (null));

const isDeletingBoard = computed(
    () =>
        currentBoard.value.type === "single" &&
        deleteTaskboardMutation.isPending.value
);

const isDeletingTask = computed(
    () => taskToDelete.value !== null && deleteTaskMutation.isPending.value
);

function retry() {
    void tasksQuery.refetch();
}

function loadMore() {
    if (!hasNextPage.value || isFetchingNextPage.value) return;

    void tasksQuery.fetchNextPage();
}

/**
 * @param {"status" | "priority"} key
 * @param {string | null} value
 */
function setFilter(key, value) {
    const nextQuery = { ...route.query };

    if (value) {
        nextQuery[key] = value;
    } else {
        delete nextQuery[key];
    }

    router.replace({ query: nextQuery });
}

/**
 * @param {TaskWithPosition} task
 */
function startDrag(task) {
    draggedTask.value = task;
}

function endDrag() {
    draggedTask.value = null;
}

/**
 * @param {TaskRead["status"]} status
 */
function isDroppable(status) {
    return draggedTask.value !== null && draggedTask.value.status !== status;
}

/**
 * @param {TaskRead} task
 * @param {TaskRead["status"]} status
 */
async function changeStatus(task, status) {
    try {
        await updateTaskMutation.mutateAsync({
            taskPublicId: task.public_id,
            payload: { status },
        });
    } catch (err) {
        showApiError(err, toast);
    }
}

/**
 * @param {TaskRead["status"]} targetStatus
 */
function dropTask(targetStatus) {
    if (!draggedTask.value) {
        return;
    }

    const task = draggedTask.value;

    draggedTask.value = null;

    return changeStatus(task, targetStatus);
}

/**
 * @param {TaskRead} task
 */
function toggleComplete(task) {
    return changeStatus(task, task.status === "done" ? "in_progress" : "done");
}

async function confirmDeleteTask() {
    if (!taskToDelete.value || !projectId.value) return;

    try {
        await deleteTaskMutation.mutateAsync({
            taskPublicId: taskToDelete.value.public_id,
            projectPublicId: projectId.value,
        });

        taskToDelete.value = null;
    } catch (err) {
        showApiError(err, toast);
    }
}

async function confirmDeleteBoard() {
    if (currentBoard.value.type !== "single") return;

    try {
        await deleteTaskboardMutation.mutateAsync(currentBoard.value.id);

        showDeleteBoard.value = false;
        router.push({ name: "taskboards-all" });
    } catch (err) {
        showApiError(err, toast);
    }
}

function openNewTask() {
    pendingTask.value = {
        title: "",
        status: "open",
    };
}

function handleClear() {
    pendingTask.value = null;
}

function refreshTaskList() {
    void tasksQuery.refetch();
}
</script>

<template>
    <v-container v-if="projectId" fluid class="task-board">
        <BoardHeader
            :board-name="taskboard?.name"
            :board-description="taskboard?.description"
            :editable="currentBoard.type === 'single' && !!boardSummary"
            @edit="showEditBoard = true"
            @delete="showDeleteBoard = true"
        />

        <BoardToolbar
            v-model:search="searchText"
            :status="statusFilter ?? undefined"
            :priority="priorityFilter ?? undefined"
            @update:status="setFilter('status', $event)"
            @update:priority="setFilter('priority', $event)"
            @new-task="openNewTask"
        />

        <main class="task-board__content">
            <v-skeleton-loader v-if="isLoading" type="article, article" />

            <div v-else-if="hasError" class="task-board__message">
                <v-icon icon="mdi-alert-circle-outline" size="32" />

                <p>We couldn't load the tasks.</p>

                <v-btn
                    color="primary"
                    variant="flat"
                    class="text-none"
                    @click="retry"
                >
                    Try again
                </v-btn>
            </div>

            <div v-else class="task-board__columns">
                <TaskColumn
                    v-for="column in STATUS_META"
                    :key="column.status"
                    :column="column"
                    :tasks="tasksByStatus[column.status] ?? []"
                    :pending-task="pendingTask"
                    :project-id="projectId"
                    :droppable="isDroppable(column.status)"
                    :taskboard-id="
                        currentBoard.type === 'single' ? currentBoard.id : null
                    "
                    @drag-start="startDrag"
                    @drag-end="endDrag"
                    @drop="dropTask"
                    @complete="toggleComplete"
                    @delete="taskToDelete = $event"
                    @task-created="refreshTaskList"
                    @clear-pending-task="handleClear"
                />
            </div>

            <div v-if="hasNextPage" class="task-board__more">
                <v-btn
                    variant="tonal"
                    color="primary"
                    class="text-none"
                    :loading="isFetchingNextPage"
                    @click="loadMore"
                >
                    Load more tasks
                </v-btn>
            </div>
        </main>

        <CreateTaskBoardModel
            :model-value="showEditBoard"
            :project-id="projectId"
            :taskboard="boardSummary"
            @close="showEditBoard = false"
        />

        <ConfirmDialog
            v-model="showDeleteBoard"
            title="Delete taskboard"
            message="Delete this taskboard? Its tasks stay in the project."
            :loading="isDeletingBoard"
            @confirm="confirmDeleteBoard"
        />

        <ConfirmDialog
            :model-value="taskToDelete !== null"
            title="Delete task"
            :message="`Delete ${taskToDelete?.title ?? 'this task'}?`"
            :loading="isDeletingTask"
            @update:model-value="taskToDelete = null"
            @confirm="confirmDeleteTask"
        />
    </v-container>

    <NoActiveProject v-else />
</template>

<style scoped>
.task-board {
    min-width: 0;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: var(--v-theme-surface, #ffffff);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.task-board__content {
    min-width: 0;
    min-height: 0;
    padding-top: 0.75rem;
}

.task-board__message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 3rem 1rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}

.task-board__more {
    display: flex;
    justify-content: center;
    padding-top: 0.75rem;
}

.task-board__columns {
    min-width: max-content;
    display: flex;
    flex-wrap: nowrap;
    align-items: stretch;
    gap: 0.75rem;
}

.task-board__columns > :deep(.task-column) {
    flex: 0 0 33%;
}

@media (min-width: 60rem) {
    .task-board {
        height: 100dvh;
    }

    .task-board__content {
        flex: 1 1 auto;
        overflow-x: auto;
        overflow-y: hidden;
    }

    .task-board__columns {
        height: 100%;
    }
}
</style>
