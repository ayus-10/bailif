<script setup>
import { ref } from "vue";
import PendingTaskCard from "@/components/tasks/PendingTaskCard.vue";
import { useTasksStore } from "@/stores/tasks.store";
import TaskCard from "./TaskCard.vue";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/project').ProjectRead} ProjectRead */

const props = defineProps({
    column: {
        type: Object,
        required: true,
    },
    tasks: {
        /** @type {import('vue').PropType<TaskRead[]>} */
        type: Array,
        required: true,
    },
    projects: {
        /** @type {import('vue').PropType<ProjectRead[]>} */
        type: Array,
        required: true,
    },
    pendingTask: {
        /** @type {import('vue').PropType<TaskCreate | null>} */
        type: Object,
        required: false,
    },
});

const store = useTasksStore();

const emit = defineEmits(["drag-start", "drop", "clear-pending-task"]);

const isDragOver = ref(false);

/** @param {DragEvent} event */
function handleDragOver(event) {
    const sourceStatus = event.dataTransfer?.getData("task-status");

    if (sourceStatus === props.column.status) {
        isDragOver.value = false;
        return;
    }

    isDragOver.value = true;
}

/** @param {DragEvent} event */
function handleDragLeave(event) {
    const target = event.currentTarget;

    if (!(target instanceof HTMLElement)) return;

    if (
        !(event.relatedTarget instanceof Node) ||
        !target.contains(event.relatedTarget)
    ) {
        isDragOver.value = false;
    }
}

/** @param {DragEvent} event */
function handleDrop(event) {
    isDragOver.value = false;

    const sourceStatus = event.dataTransfer?.getData("task-status");

    if (sourceStatus === props.column.status) {
        return;
    }

    emit("drop", props.column.status);
}

/**
 * @param {DragEvent} event
 * @param {TaskRead} task
 */
function handleDragStart(event, task) {
    event.dataTransfer?.setData("task-status", task.status);
    emit("drag-start", task);
}

function handleDragEnd() {
    isDragOver.value = false;
}

/** @param {TaskCreate} task */
async function handleCreate(task) {
    await store.create("default", task);
    emit("clear-pending-task");
}

function handleCancel() {
    emit("clear-pending-task");
}
</script>

<template>
    <v-col cols="12" md="4">
        <div class="d-flex align-center mb-2">
            <v-icon :icon="column.icon" size="18" class="mr-2" />

            <span class="text-subtitle-2 font-weight-medium">
                {{ column.label }}
            </span>

            <v-chip size="x-small" class="ml-2">
                {{ tasks.length }}
            </v-chip>
        </div>

        <div
            class="task-column"
            :class="{ 'task-column--drag-over': isDragOver }"
            @dragover.prevent="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
        >
            <PendingTaskCard
                v-if="pendingTask && pendingTask.status === column.status"
                :projects="projects"
                @submit="handleCreate"
                @cancel="handleCancel"
            />

            <TaskCard
                v-for="task in tasks"
                :key="task.id"
                :task="task"
                draggable="true"
                @dragstart="handleDragStart($event, task)"
                @dragend="handleDragEnd"
            />

            <v-sheet
                v-if="tasks.length === 0"
                class="task-column__empty text-center text-caption text-medium-emphasis"
                border
                rounded
            >
                No tasks here
            </v-sheet>
        </div>
    </v-col>
</template>

<style scoped>
.task-column {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 100%;
    padding: 10px;
    gap: 10px;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-radius: 10px;
    background: rgba(var(--v-theme-on-surface), 0.015);
    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease;
}

.task-column__empty {
    margin-top: auto;
    margin-bottom: auto;
}

.task-column--drag-over {
    background: rgba(var(--v-theme-primary), 0.06);
    border-color: rgba(var(--v-theme-primary), 0.4);
    box-shadow:
        inset 0 0 0 1px rgba(var(--v-theme-primary), 0.12),
        0 0 0 2px rgba(var(--v-theme-primary), 0.04);
}
</style>
