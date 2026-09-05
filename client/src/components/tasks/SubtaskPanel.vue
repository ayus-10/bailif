<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref, watch } from "vue";
import PendingTaskCard from "@/components/tasks/PendingTaskCard.vue";
import TaskCard from "@/components/tasks/TaskCard.vue";
import { useProjectsStore } from "@/stores/projects.store";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/shared').FetchStatus} FetchStatus */

const props = defineProps({
    taskId: {
        type: String,
        required: true,
    },
    projectId: {
        type: String,
        required: true,
    },
});

const route = useRoute();
const router = useRouter();
const tasksStore = useTasksStore();
const projectsStore = useProjectsStore();

const boardId = computed(() => `board-${props.taskId}`);

function fetchSubtasks() {
    tasksStore.fetch(boardId.value, {
        queryMode: "child-tasks",
        parentId: props.taskId,
    });
}

function fetchProjects() {
    projectsStore.fetch();
}

onMounted(() => {
    fetchSubtasks();
    fetchProjects();
});

watch(
    () => props.taskId,
    (newId, oldId) => {
        if (newId && newId !== oldId) {
            fetchSubtasks();
        }
    }
);

/** @type {import('vue').ComputedRef<TaskRead[]>} */
const subtasks = computed(() => tasksStore.items[boardId.value] ?? []);

const hasSubtasks = computed(() => subtasks.value.length > 0);

const projects = computed(() => projectsStore.items ?? []);

/** @type {import('vue').ComputedRef<FetchStatus>} */
const fetchStatus = computed(() => tasksStore.status[boardId.value] ?? "idle");
const isLoading = computed(
    () =>
        fetchStatus.value === "loading" || fetchStatus.value === "loading-more"
);
const fetchError = computed(() => tasksStore.errors[boardId.value] ?? null);

/** @type {import('vue').Ref<TaskCreate | null>} */
const pendingSubTask = ref(null);

const showSubtasks = computed(
    () => !isLoading.value && !fetchError.value && hasSubtasks.value
);
const showEmptyMessage = computed(
    () => !showSubtasks.value && !pendingSubTask.value
);

/** @param {TaskRead} subtask */
function openSubtask(subtask) {
    router.push({
        name: route.name,
        params: { ...route.params, id: subtask.id },
    });
}

/** @param {TaskCreate} task */
async function handleCreateSubtask(task) {
    if (!pendingSubTask.value) return;
    await tasksStore.create(task);
    pendingSubTask.value = null;
}

function handleNewSubtask() {
    pendingSubTask.value = {
        title: "",
        project_id: props.projectId,
        status: "open",
    };
}

function handleClear() {
    pendingSubTask.value = null;
}
</script>

<template>
    <section class="panel subtask-panel">
        <div class="panel__heading">
            <h2 class="panel__label">
                Subtasks
                <span v-if="hasSubtasks" class="subtask-panel__count">
                    {{ subtasks.length }}
                </span>
            </h2>

            <v-btn
                variant="text"
                density="comfortable"
                size="small"
                prepend-icon="mdi-plus"
                aria-label="Add subtask"
                @click="handleNewSubtask"
            >
                Add subtask
            </v-btn>
        </div>

        <div v-if="isLoading" class="subtask-panel__loading">
            <v-progress-circular indeterminate size="20" width="2" />
        </div>

        <div v-else-if="fetchError" class="subtask-panel__error">
            <span>Couldn't load subtasks.</span>

            <v-btn
                variant="text"
                density="comfortable"
                size="small"
                @click="fetchSubtasks"
            >
                Retry
            </v-btn>
        </div>

        <p v-if="showEmptyMessage" class="panel__empty">No subtasks yet.</p>

        <PendingTaskCard
            v-if="pendingSubTask"
            :projects="projects"
            :parent-id="props.taskId"
            @submit="handleCreateSubtask"
            @cancel="handleClear"
        />

        <TaskCard
            v-if="showSubtasks"
            v-for="subtask in subtasks"
            :key="subtask.id"
            :task="subtask"
            class="subtask-list__card"
            @click="openSubtask(subtask)"
        />
    </section>
</template>

<style scoped>
.panel {
    padding: 16px 18px;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-radius: 10px;
    background: rgb(var(--v-theme-surface));
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.035);
    transition:
        border-color 140ms ease,
        box-shadow 140ms ease;
}

.panel:hover {
    border-color: rgba(var(--v-theme-on-surface), 0.12);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
}

.panel__label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
    color: rgba(var(--v-theme-on-surface), 0.55);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    line-height: 1.4;
    text-transform: uppercase;
}

.panel__empty {
    margin: 0;
    color: rgba(var(--v-theme-on-surface), 0.5);
    font-size: 0.875rem;
    font-style: italic;
}

.subtask-panel__count {
    padding: 1px 7px;
    border-radius: 999px;
    background: rgba(var(--v-theme-on-surface), 0.08);
    color: rgba(var(--v-theme-on-surface), 0.65);
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: normal;
    text-transform: none;
}

.subtask-panel__loading {
    display: flex;
    justify-content: center;
    padding: 12px 0;
}

.subtask-panel__error {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 10px;
    border-radius: 6px;
    background: rgba(var(--v-theme-error), 0.06);
    color: rgb(var(--v-theme-error));
    font-size: 0.8125rem;
}

.subtask-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.subtask-list__card {
    cursor: pointer;
}
</style>
