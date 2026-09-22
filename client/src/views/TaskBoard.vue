<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, ref, watch } from "vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import BoardHeader from "@/components/taskboards/BoardHeader.vue";
import BoardToolbar from "@/components/taskboards/BoardToolbar.vue";
import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { TASK_COLUMNS } from "@/constants/tasks";
import { useTaskboardsStore } from "@/stores/taskboards.store";
import { useTasksStore } from "@/stores/tasks.store";
import { showApiError } from "@/utils/errorHandlers";

/**
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

const taskboardsStore = useTaskboardsStore();
const tasksStore = useTasksStore();

watch(
    [projectId, query],
    ([id, currentQuery]) => {
        if (!id) return;

        tasksStore.fetch(id, currentQuery);
    },
    { immediate: true }
);

watch(currentBoard, fetchCurrentBoard, { immediate: true });

const taskboard = computed(() => taskboardsStore.currentTaskboard);

const tasks = computed(() =>
    projectId.value ? tasksStore.tasksByQuery(projectId.value, query.value) : []
);

const filteredTasks = computed(() => {
    return tasks.value.filter((task) => {
        if (route.query.status && task.status !== route.query.status) {
            return false;
        }

        if (route.query.priority && task.priority !== route.query.priority) {
            return false;
        }

        return true;
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

/**
 * @param {String} action
 */
function handleBoardAction(action) {
    console.log(action);
}

/**
 * @param {String} action
 */
function handleToolbarAction(action) {
    console.log(action);
}

/**
 * @param {BoardSelection} board
 */
function fetchCurrentBoard(board) {
    if (board.type === "single") {
        taskboardsStore.get(board.id);
        return;
    }
    taskboardsStore.currentTaskboard = null;
}

function retry() {
    if (!projectId.value) return;

    if (currentBoard.value.type === "single" && currentBoard.value.id) {
        taskboardsStore.get(currentBoard.value.id, {
            forceRefresh: true,
        });
    }

    tasksStore.fetch(projectId.value, {
        ...query.value,
        forceRefresh: true,
    });
}

/**
 * @param {string} key
 */
function clearFilter(key) {
    const nextQuery = { ...route.query };

    delete nextQuery[key];

    router.push({
        path: route.path,
        query: nextQuery,
    });
}

/**
 * @param {TaskWithPosition} task
 */
function startDrag(task) {
    draggedTask.value = task;
}

/**
 * @param {TaskWithPosition["status"]} targetStatus
 */
async function dropTask(targetStatus) {
    if (!draggedTask.value) {
        return;
    }

    const task = draggedTask.value;

    if (task.status === targetStatus) {
        draggedTask.value = null;
        return;
    }

    const oldStatus = task.status;

    task.status = targetStatus;

    try {
        await tasksStore.update(task.public_id, {
            status: targetStatus,
        });
    } catch (err) {
        task.status = oldStatus;
        showApiError(err, toast);
    } finally {
        draggedTask.value = null;
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
</script>

<template>
    <v-container v-if="projectId" fluid class="task-board">
        <BoardHeader
            @action="handleBoardAction"
            :board-name="taskboard?.name"
            :board-description="taskboard?.description"
        />

        <BoardToolbar @action="handleToolbarAction" @new-task="openNewTask" />

        <main class="task-board__content">
            <div class="task-board__columns">
                <TaskColumn
                    v-for="column in TASK_COLUMNS"
                    :key="column.status"
                    :column="column"
                    :tasks="tasksByStatus[column.status] ?? []"
                    :pending-task="pendingTask"
                    :project-id="projectId"
                    :taskboard-id="
                        currentBoard.type === 'single' ? currentBoard.id : null
                    "
                    @drag-start="startDrag"
                    @drop="dropTask"
                    @clear-pending-task="handleClear"
                />
            </div>
        </main>
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
