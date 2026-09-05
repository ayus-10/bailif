<script setup>
import { ref } from "vue";
import PendingTaskCard from "@/components/tasks/PendingTaskCard.vue";
import { useTaskboardsStore } from "@/stores/taskboard.store";
import { useTasksStore } from "@/stores/tasks.store";
import TaskCard from "./TaskCard.vue";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/project').ProjectRead} ProjectRead */

const COLUMN_CONFIG = {
    iconSize: "1.125rem",
    countChipSize: "x-small",
    menuIcon: "mdi-dots-horizontal",
    menuButtonSize: "small",
    emptyStateIcon: "mdi-inbox-outline",
    emptyStateIconSize: "1.25rem",
    resizeLabel: "Resize column",
};

const props = defineProps({
    column: {
        type: Object,
        required: true,
    },
    projectId: {
        type: String,
    },
    taskboardId: {
        type: [String, null],
        default: null,
    },
    tasks: {
        /** @type {import('vue').PropType<TaskRead[]>} */
        type: Array,
        required: true,
    },
    pendingTask: {
        /** @type {import('vue').PropType<TaskCreate | null>} */
        type: Object,
        required: false,
    },
});

const tasksStore = useTasksStore();
const taskboardsStore = useTaskboardsStore();

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

/** @param {TaskCreate} payload */
async function handleCreate(payload) {
    const task = await tasksStore.create(payload);

    if (!task) return;

    if (props.taskboardId)
        await taskboardsStore.addTask(props.taskboardId, { task_id: task.id });

    emit("clear-pending-task");
}

function handleCancel() {
    emit("clear-pending-task");
}
</script>

<template>
    <v-sheet class="task-column" rounded border>
        <div class="task-column__header">
            <div class="d-flex align-center">
                <v-icon
                    :icon="column.icon"
                    :size="COLUMN_CONFIG.iconSize"
                    class="mr-2"
                />

                <span class="text-subtitle-2 font-weight-medium">
                    {{ column.label }}
                </span>

                <v-chip :size="COLUMN_CONFIG.countChipSize" class="ml-2">
                    {{ tasks.length }}
                </v-chip>
            </div>

            <v-btn
                :icon="COLUMN_CONFIG.menuIcon"
                :size="COLUMN_CONFIG.menuButtonSize"
                variant="text"
            />
        </div>

        <v-divider />

        <div
            class="task-column__body"
            @dragover.prevent="handleDragOver"
            @dragleave="handleDragLeave"
            @drop="handleDrop"
        >
            <PendingTaskCard
                v-if="pendingTask?.status === column.status"
                :project-id="props.projectId"
                :taskboard-id="props.taskboardId"
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
                v-if="
                    tasks.length === 0 && pendingTask?.status !== column.status
                "
                class="task-column__empty"
                border
                rounded
            >
                <v-icon
                    :icon="COLUMN_CONFIG.emptyStateIcon"
                    :size="COLUMN_CONFIG.emptyStateIconSize"
                />

                <span class="text-caption text-medium-emphasis">
                    {{ column.emptyLabel }}
                </span>
            </v-sheet>
        </div>

        <div
            class="task-column__resize-handle"
            role="separator"
            :aria-label="COLUMN_CONFIG.resizeLabel"
        />
    </v-sheet>
</template>

<style scoped>
.task-column {
    position: relative;
    flex: 0 0 33.333%;
    min-width: 18rem;
    max-width: 48rem;
    min-height: 0;
    display: flex;
    flex-direction: column;
}

.task-column__header {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.task-column__body {
    flex: 1 1 auto;
    min-height: 0;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.task-column__empty {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 6rem;
}

.task-column__resize-handle {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    width: 0.375rem;
    cursor: col-resize;
    user-select: none;
    touch-action: none;
}
</style>
