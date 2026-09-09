<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref, watch } from "vue";
import PendingTaskCard from "@/components/tasks/PendingTaskCard.vue";
import TaskCard from "@/components/tasks/TaskCard.vue";
import { useProjectsStore } from "@/stores/projects.store";
import { useTasksStore } from "@/stores/tasks.store";
import EmptyPanel from "./EmptyPanel.vue";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskCreate} TaskCreate */
/** @typedef {import("@/types/shared").FetchStatus} FetchStatus */

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

/** @type {import("vue").ComputedRef<TaskRead[]>} */
const subtasks = computed(() => tasksStore.items[boardId.value] ?? []);

const hasSubtasks = computed(() => subtasks.value.length > 0);

const projects = computed(() => projectsStore.items ?? []);

/** @type {import("vue").ComputedRef<FetchStatus>} */
const fetchStatus = computed(() => tasksStore.status[boardId.value] ?? "idle");
const isLoading = computed(
    () =>
        fetchStatus.value === "loading" || fetchStatus.value === "loading-more"
);
const fetchError = computed(() => tasksStore.errors[boardId.value] ?? null);

/** @type {import("vue").Ref<TaskCreate | null>} */
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
                v-if="hasSubtasks"
                variant="tonal"
                color="primary"
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

        <EmptyPanel
            v-if="showEmptyMessage"
            message="No subtasks yet - click to add some"
            @click="handleNewSubtask"
        />

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
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    padding: 0.875rem 1rem;
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    transition: border-color 0.12s ease;
}

.panel:hover {
    border-color: rgb(var(--v-theme-outline, 225, 228, 232));
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    min-height: 1.5rem;
}

.panel__label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
}

.subtask-panel__count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.25rem;
    height: 1.25rem;
    padding: 0 0.375rem;
    border-radius: 999px;
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    user-select: none;
    -webkit-user-select: none;
}

.subtask-panel__loading {
    display: flex;
    justify-content: center;
    padding: 0.75rem 0;
}

.subtask-panel__error {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0.625rem;
    border-radius: 0.5rem;
    background: rgba(var(--v-theme-error), 0.06);
    color: rgb(var(--v-theme-error));
    font-size: 0.8125rem;
    font-weight: 500;
}

.subtask-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.625rem;
}

.subtask-list__card {
    cursor: pointer;
}
</style>
