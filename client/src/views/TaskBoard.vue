<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { TASK_COLUMNS } from "@/constants/tasks";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/task').TaskQueryMode} TaskQueryMode */

const BOARD_CONFIG = {
    createButton: {
        label: "Create task",
        icon: "mdi-plus",
        color: "primary",
    },
    column: {
        initialWidth: "33.333%",
        minWidth: "18rem",
        maxWidth: "48rem",
    },
};

const board = {
    name: "Project Tasks",
    description: "Plan, prioritize, and track work across the project.",
};

const route = useRoute();
const router = useRouter();

const projectId = ref(localStorage.getItem("project_id") ?? ""); // TODO: replace with session

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
const preferredQueryMode = ref("root-tasks"); // TODO: it was supposed to allow all, but wtf is going on?

const query = computed(() => ({
    queryMode: preferredQueryMode.value,
    taskboardId:
        currentBoard.value.type === "board" ? currentBoard.value.id : null,
    // TODO: add more TaskFetchOptions
}));

const tasksStore = useTasksStore();

onMounted(() => {
    tasksStore.fetch(projectId.value, query.value);
});

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
        if (route.query.status && task.status !== route.query.status)
            return false;

        if (route.query.priority && task.priority !== route.query.priority)
            return false;

        return true;
    });
});

const tasksByStatus = computed(() => {
    return filteredTasks.value.reduce((acc, task) => {
        if (!acc[task.status]) acc[task.status] = [];

        acc[task.status].push(task);
        return acc;
    }, /** @type {Record<string, TaskRead[]>} */ ({}));
});

const draggedTask = ref(/** @type {TaskRead | null} */ (null));

/** @type {import('vue').Ref<TaskCreate | null>} */
const pendingTask = ref(null);

function retry() {
    tasksStore.fetch(projectId.value, { ...query.value, forceRefresh: true });
}

/** @param {string} key */
function clearFilter(key) {
    const query = { ...route.query };

    delete query[key];

    router.push({
        path: route.path,
        query,
    });
}

/** @param {TaskRead} task */
function startDrag(task) {
    draggedTask.value = task;
}

/** @param {TaskRead["status"]} targetStatus */
async function dropTask(targetStatus) {
    if (!draggedTask.value) return;

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
        <div class="task-board__header">
            <div>
                <h1 class="text-h6 font-weight-bold">
                    {{ board.name }}
                </h1>

                <p class="text-caption text-medium-emphasis mb-0 mt-1">
                    {{ board.description }}
                </p>
            </div>

            <v-btn
                :color="BOARD_CONFIG.createButton.color"
                :prepend-icon="BOARD_CONFIG.createButton.icon"
                variant="flat"
                density="comfortable"
                class="text-none font-weight-medium"
                @click="openNewTask"
            >
                {{ BOARD_CONFIG.createButton.label }}
            </v-btn>
        </div>

        <div class="task-board__content">
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
        </div>
    </v-container>
</template>

<style scoped>
.task-board {
    height: 100%;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.task-board__header {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.task-board__content {
    flex: 1 1 auto;
    min-height: 0;
    min-width: 0;
    overflow-x: auto;
    overflow-y: hidden;
}

.task-board__columns {
    height: 100%;
    min-width: max-content;
    display: flex;
    flex-wrap: nowrap;
    align-items: stretch;
    gap: 1rem;
}

.task-board__columns > :deep(.task-column) {
    flex: 0 0 33.333%;
}
</style>
