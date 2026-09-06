<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import BoardHeader from "@/components/taskboards/BoardHeader.vue";
import BoardToolbar from "@/components/taskboards/BoardToolbar.vue";
import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { TASK_COLUMNS } from "@/constants/tasks";
import { useTaskboardsStore } from "@/stores/taskboard.store";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/task').TaskQueryMode} TaskQueryMode */

const route = useRoute();
const router = useRouter();

const projectId = ref(localStorage.getItem("project_id") ?? "");

const currentBoard = computed(() => {
    const id = route.params.id;

    if (!id || id === "all") {
        return { type: "all" };
    }

    return {
        type: "board",
        id: Array.isArray(id) ? id[0] : id,
    };
});

/** @type {import('vue').Ref<TaskQueryMode>} */
const preferredQueryMode = ref("root-tasks");

const query = computed(() => ({
    queryMode: preferredQueryMode.value,
    taskboardId:
        currentBoard.value.type === "board" ? currentBoard.value.id : null,
}));

const taskboardsStore = useTaskboardsStore();
const tasksStore = useTasksStore();

onMounted(() => {
    if (currentBoard.value.type === "board" && currentBoard.value.id) {
        taskboardsStore.get(currentBoard.value.id);
    }

    tasksStore.fetch(projectId.value, query.value);
});

const taskboard = computed(() => taskboardsStore.currentTaskboard);

const tasks = computed(() =>
    tasksStore.tasksByQuery(projectId.value, query.value)
);

const status = computed(() =>
    tasksStore.statusByQuery(projectId.value, query.value)
);

const error = computed(() =>
    tasksStore.errorByQuery(projectId.value, query.value)
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
    return filteredTasks.value.reduce((acc, task) => {
        if (!acc[task.status]) {
            acc[task.status] = [];
        }

        acc[task.status].push(task);

        return acc;
    }, /** @type {Record<string, TaskRead[]>} */ ({}));
});

const draggedTask = ref(/** @type {TaskRead | null} */ (null));

/** @type {import('vue').Ref<TaskCreate | null>} */
const pendingTask = ref(null);
/** @param {String} action */
function handleBoardAction(action) {
    console.log(action);
}
/** @param {String} action */
function handleToolbarAction(action) {
    console.log(action);
}

function retry() {
    if (currentBoard.value.type === "board" && currentBoard.value.id) {
        taskboardsStore.get(currentBoard.value.id, {
            forceRefresh: true,
        });
    }

    tasksStore.fetch(projectId.value, {
        ...query.value,
        forceRefresh: true,
    });
}

/** @param {string} key */
function clearFilter(key) {
    const nextQuery = { ...route.query };

    delete nextQuery[key];

    router.push({
        path: route.path,
        query: nextQuery,
    });
}

/** @param {TaskRead} task */
function startDrag(task) {
    draggedTask.value = task;
}

/** @param {TaskRead["status"]} targetStatus */
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
        await tasksStore.update(task.id, {
            status: targetStatus,
        });
    } catch (err) {
        task.status = oldStatus;
        console.error(err);
    } finally {
        draggedTask.value = null;
    }
}

function openNewTask() {
    pendingTask.value = {
        project_id: projectId.value,
        title: "",
        status: "open",
    };
}

function handleClear() {
    pendingTask.value = null;
}
</script>

<template>
    <v-container fluid class="task-board">
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
                        currentBoard.type === 'board' ? currentBoard.id : null
                    "
                    @drag-start="startDrag"
                    @drop="dropTask"
                    @clear-pending-task="handleClear"
                />
            </div>
        </main>
    </v-container>
</template>

<style scoped>
.task-board {
    height: 100%;
    min-width: 0;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: var(--v-theme-surface, #ffffff);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.task-board__content {
    flex: 1 1 auto;
    min-height: 0;
    min-width: 0;
    padding-top: 0.75rem;
    overflow-x: auto;
    overflow-y: hidden;
}

.task-board__columns {
    height: 100%;
    min-width: max-content;
    display: flex;
    flex-wrap: nowrap;
    align-items: stretch;
    gap: 0.75rem;
}

.task-board__columns > :deep(.task-column) {
    flex: 0 0 33%;
}
</style>
