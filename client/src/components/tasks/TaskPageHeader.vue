<script setup>
import EditableVChip from "@/components/common/EditableVChip.vue";
import { STATUS_META, TASK_PRIORITIES } from "@/constants/taskMeta";
import { PRIORITY_COLORS, PRIORITY_ICONS } from "@/constants/tasks";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskDraft} TaskDraft */
/** @typedef {import("@/types/shared").EditMode} EditMode */
/** @typedef {TaskRead["status"]} TaskStatus */
/** @typedef {TaskRead["priority"]} TaskPriority */

defineProps({
    task: {
        /** @type {import("vue").PropType<TaskRead>} */
        type: Object,
        required: true,
    },
    editMode: {
        type: /** @type {import("vue").PropType<EditMode>} */ (String),
        required: true,
    },
    draft: {
        /** @type {import("vue").PropType<TaskDraft>} */
        type: Object,
        required: true,
    },
    selectedStatus: {
        type: /** @type {import("vue").PropType<TaskStatus | null>} */ (String),
        required: true,
    },

    selectedPriority: {
        type: /** @type {import("vue").PropType<TaskPriority | null>} */ (
            String
        ),
        required: true,
    },
    statusOptions: {
        /** @type {import("vue").PropType<TaskStatus[]>} */
        type: Array,
        required: true,
    },
    priorityOptions: {
        /** @type {import("vue").PropType<TaskPriority[]>} */
        type: Array,
        required: true,
    },
    isSaving: Boolean,
    isSavingStatus: Boolean,
    isSavingPriority: Boolean,
    hasPendingChanges: Boolean,
    isOverdue: Boolean,
    isEditingTitle: Boolean,
});

const emit = defineEmits([
    "back",
    "edit",
    "cancel",
    "save",
    "status-change",
    "priority-change",
]);
</script>

<template>
    <div class="task-page__topbar">
        <v-btn
            icon="mdi-arrow-left"
            variant="text"
            density="comfortable"
            aria-label="Go back"
            @click="emit('back')"
        />

        <v-spacer />

        <div v-if="editMode !== 'none'" class="task-page__actions">
            <v-btn
                variant="text"
                density="comfortable"
                :disabled="isSaving"
                @click="emit('cancel')"
            >
                Cancel
            </v-btn>

            <v-btn
                color="primary"
                variant="tonal"
                density="comfortable"
                prepend-icon="mdi-content-save-outline"
                :disabled="!hasPendingChanges"
                :loading="isSaving"
                @click="emit('save')"
            >
                Save
            </v-btn>
        </div>
    </div>

    <header class="task-page__header">
        <div
            class="editable-field editable-field--title"
            :class="{
                'editable-field--editing': isEditingTitle,
            }"
        >
            <v-text-field
                v-if="isEditingTitle"
                v-model="draft.title"
                label="Title"
                variant="outlined"
                density="comfortable"
                hide-details
                autofocus
                @keydown.escape="emit('cancel')"
            />

            <div v-else class="editable-field__display">
                <h1 class="task-page__title">
                    {{ task.title }}
                </h1>

                <v-btn
                    icon="mdi-pencil-outline"
                    size="x-small"
                    variant="text"
                    density="comfortable"
                    aria-label="Edit title"
                    @click="emit('edit', 'title')"
                />
            </div>
        </div>

        <div class="task-page__badges">
            <EditableVChip
                :model-value="selectedStatus"
                :items="
                    Object.entries(STATUS_META).map(([value, meta]) => ({
                        value,
                        label: meta.label,
                        color: meta.color,
                        icon: meta.icon,
                    }))
                "
                :disabled="isSavingStatus"
                size="small"
                variant="tonal"
                @update:model-value="
                    (/** @type {TaskStatus} */ value) =>
                        (selectedStatus = value)
                "
                @change="emit('status-change', $event)"
            />

            <EditableVChip
                :model-value="selectedPriority ?? undefined"
                :items="
                    TASK_PRIORITIES.map((value) => ({
                        value,
                        label: value.toUpperCase(),
                        color: PRIORITY_COLORS[value],
                        icon: PRIORITY_ICONS[value],
                    }))
                "
                :disabled="isSavingPriority"
                size="small"
                variant="tonal"
                @change="emit('priority-change', $event)"
            />

            <span v-if="isOverdue" class="task-page__overdue-flag">
                <v-icon icon="mdi-calendar-alert" size="15" />
                Overdue
            </span>
        </div>
    </header>
</template>

<style scoped>
.task-page__topbar {
    display: flex;
    align-items: center;
    padding: 0.5rem 0.75rem;
    border-bottom: 0.0625rem solid
        rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.task-page__actions {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.task-page__header {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1.25rem 1.5rem 0.5rem;
}

.editable-field--title {
    max-width: 40rem;
}

.editable-field__display {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.task-page__title {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.5rem;
}

.editable-field__edit-btn {
    opacity: 0;
    transition: opacity 0.12s ease;
}

.editable-field--title:hover .editable-field__edit-btn,
.editable-field__edit-btn:focus-visible {
    opacity: 1;
}

.editable-field__edit-btn:deep(.v-icon) {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
}

.editable-field__edit-btn:hover:deep(.v-icon) {
    color: #1976d2;
}

.editable-field--title :deep(.v-field--variant-outlined .v-field__outline) {
    color: rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.editable-field--title
    :deep(.v-field--variant-outlined.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-on-surface));
}

.task-page__badges {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.task-page__overdue-flag {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.625rem;
    border-radius: 999px;
    background: rgba(var(--v-theme-error), 0.08);
    color: rgb(var(--v-theme-error));
    font-size: 0.75rem;
    font-weight: 700;
    user-select: none;
    -webkit-user-select: none;
}
</style>
