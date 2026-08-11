<script setup>
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

/**
 * @param {TaskRead} task
 */
function handleDragStart(task) {
    emit("drag-start", task);
}

function handleDrop() {
    emit("drop", props.column.status);
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
            class="d-flex flex-column ga-3"
            @dragover.prevent
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
                @dragstart="handleDragStart(task)"
            />

            <v-sheet
                v-if="tasks.length === 0"
                class="pa-4 mt-3 text-center text-caption text-medium-emphasis"
                border
                rounded
            >
                No tasks here
            </v-sheet>
        </div>
    </v-col>
</template>
