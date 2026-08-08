<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { TASK_COLUMNS } from "@/constants/tasks";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskRead} TaskCreate*/

const route = useRoute();
const router = useRouter();

const store = useTasksStore();

const boardId = computed(() => String(route.params.boardId ?? "default"));

onMounted(() => {
    store.fetch(boardId.value);
});

const tasks = computed(() => store.items[boardId.value] ?? []);

const status = computed(() => store.status[boardId.value] ?? "idle");

const error = computed(() => store.errors[boardId.value]);

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
        (acc[task.status] ??= []).push(task);

        return acc;
    }, /** @type {Record<string, TaskRead[]>} */ ({}));
});

function retry() {
    store.fetch(boardId.value, {
        force: true,
    });
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

const draggedTask = ref(/** @type {TaskRead | null} */ (null));

/**
 * @param {TaskRead} task
 */
function startDrag(task) {
    draggedTask.value = task;
}

/**
 * @param {string} targetStatus
 */
async function dropTask(targetStatus) {
    if (!draggedTask.value) return;

    const task = draggedTask.value;

    if (task.status === targetStatus) {
        draggedTask.value = null;
        return;
    }

    // optimistic update
    const oldStatus = task.status;
    task.status = targetStatus;

    try {
        // await store.update(boardId.value, task.id, {
        //     status: targetStatus,
        // });
    } catch (err) {
        // rollback
        task.status = oldStatus;
        console.error(err);
    } finally {
        draggedTask.value = null;
    }
}

const pendingTask = ref(null);

function openNewTask() {
    pendingTask.value = {
        status: "open",
    };
}

/** @param {TaskCreate} task */
function createTask(task) {
    console.log(task);

    // await store.create(boardId.value, task)

    showNewTask.value = false;
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Task Board</h1>
                <span class="text-body-2 text-medium-emphasis">
                    {{ filteredTasks.length }} task{{
                        filteredTasks.length === 1 ? "" : "s"
                    }}
                    <span v-if="route.query.status || route.query.priority">
                        matching filters
                    </span>
                </span>
            </div>
            <v-spacer />
            <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                variant="flat"
                @click="openNewTask"
                >New Task
            </v-btn>
        </div>

        <div v-if="route.query.status || route.query.priority" class="mb-4">
            <v-chip
                v-if="route.query.status"
                closable
                size="small"
                class="mr-2"
                @click:close="clearFilter('status')"
            >
                Status: {{ route.query.status }}
            </v-chip>
            <v-chip
                v-if="route.query.priority"
                closable
                size="small"
                @click:close="clearFilter('priority')"
            >
                Priority: {{ route.query.priority }}
            </v-chip>
        </div>

        <div v-if="status === 'loading'" class="d-flex justify-center py-12">
            <v-progress-circular indeterminate />
        </div>

        <v-alert v-else-if="status === 'error'" type="error" class="mb-4">
            {{ error?.message }}

            <template #append>
                <v-btn size="small" @click="retry"> Retry </v-btn>
            </template>
        </v-alert>

        <v-row v-else>
            <TaskColumn
                v-for="column in TASK_COLUMNS"
                :key="column.status"
                :column="column"
                :tasks="tasksByStatus[column.status] ?? []"
                :pendingTask="pendingTask"
                @drag-start="startDrag"
                @drop="dropTask"
            />
        </v-row>
    </v-container>
</template>
