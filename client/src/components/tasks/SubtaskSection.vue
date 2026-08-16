<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, watch } from "vue";
import TaskCard from "@/components/tasks/TaskCard.vue";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/shared').FetchStatus} FetchStatus */

const props = defineProps({
    taskId: {
        type: String,
        required: true,
    },
});

const emit = defineEmits(["add-subtask"]);

const route = useRoute();
const router = useRouter();
const tasksStore = useTasksStore();

const boardId = computed(() => `board-${props.taskId}`);

function fetchSubtasks() {
    tasksStore.fetch(boardId.value, {
        parentId: props.taskId,
    });
}

onMounted(fetchSubtasks);

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

/** @type {import('vue').ComputedRef<FetchStatus>} */
const fetchStatus = computed(() => tasksStore.status[boardId.value] ?? "idle");
const isLoading = computed(
    () =>
        fetchStatus.value === "loading" || fetchStatus.value === "loading-more"
);
const fetchError = computed(() => tasksStore.errors[boardId.value] ?? null);

/** @param {TaskRead} subtask */
function openSubtask(subtask) {
    router.push({
        name: route.name,
        params: { ...route.params, id: subtask.id },
    });
}

function handleAddSubtask() {
    emit("add-subtask", { parentId: props.taskId });
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
                @click="handleAddSubtask"
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

        <div v-else-if="hasSubtasks" class="subtask-list">
            <TaskCard
                v-for="subtask in subtasks"
                :key="subtask.id"
                :task="subtask"
                class="subtask-list__card"
                @click="openSubtask(subtask)"
            />
        </div>

        <p v-else class="panel__empty">No subtasks yet.</p>
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
