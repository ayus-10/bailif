<script setup>
import EditableVChip from "@/components/common/EditableVChip.vue";
import { STATUS_META, TASK_PRIORITIES } from "@/constants/taskMeta";
import {
    PRIORITY_COLORS,
    PRIORITY_ICONS,
    PRIORITY_LABELS,
} from "@/constants/tasks";
import TaskBreadcrumbs from "./TaskBreadcrumbs.vue";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskDraft} TaskDraft */
/** @typedef {import("@/types/shared").EditMode} EditMode */

const props = defineProps({
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
        type: /** @type {import("vue").PropType<TaskRead["status"] | null>} */ (
            String
        ),
        default: null,
    },
    selectedPriority: {
        type: /** @type {import("vue").PropType<TaskRead["priority"] | null>} */ (
            String
        ),
        default: null,
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
    "duplicate",
    "delete",
]);
</script>

<template>
    <div class="task-page__topbar">
        <TaskBreadcrumbs :task="task" @back="emit('back')" />

        <v-spacer />

        <div class="task-page__actions">
            <v-btn
                variant="plain"
                density="comfortable"
                prepend-icon="mdi-share-variant-outline"
            >
                Share
            </v-btn>

            <v-menu>
                <template #activator="{ props: menuProps }">
                    <v-btn
                        v-bind="menuProps"
                        icon="mdi-dots-horizontal"
                        variant="plain"
                        density="comfortable"
                        aria-label="More actions"
                    />
                </template>

                <v-list density="compact">
                    <v-list-item
                        prepend-icon="mdi-pencil-outline"
                        title="Edit task"
                        @click="emit('edit', 'title')"
                    />
                    <v-list-item
                        prepend-icon="mdi-content-copy"
                        title="Duplicate task"
                        @click="emit('duplicate')"
                    />
                    <v-divider />
                    <v-list-item
                        prepend-icon="mdi-delete-outline"
                        title="Delete task"
                        class="task-page__delete-item"
                        @click="emit('delete')"
                    />
                </v-list>
            </v-menu>
        </div>
    </div>

    <header class="task-page__header">
        <div class="task-page__identity">
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
                        class="editable-field__edit-btn"
                        icon="mdi-pencil-outline"
                        size="x-small"
                        variant="text"
                        density="comfortable"
                        aria-label="Edit title"
                        @click="emit('edit', 'title')"
                    />
                </div>
            </div>
        </div>

        <div class="task-page__badges">
            <span v-if="isOverdue" class="task-page__overdue-flag">
                <v-icon icon="mdi-calendar-alert" size="14" />
                Overdue
            </span>

            <EditableVChip
                :model-value="selectedStatus ?? undefined"
                :items="
                    Object.entries(STATUS_META).map(([value, meta]) => ({
                        value,
                        label: meta.label,
                        color: meta.color,
                        icon: meta.icon,
                    }))
                "
                :disabled="isSavingStatus"
                size="default"
                rounded="lg"
                variant="tonal"
                class="task-page__chip"
                @update:model-value="
                    (/** @type {TaskRead['status']} */ value) =>
                        (selectedStatus = value)
                "
                @change="emit('status-change', $event)"
            />

            <EditableVChip
                :model-value="selectedPriority ?? undefined"
                :items="
                    TASK_PRIORITIES.map((value) => ({
                        value,
                        label: PRIORITY_LABELS[value],
                        color: PRIORITY_COLORS[value],
                        icon: PRIORITY_ICONS[value],
                    }))
                "
                :disabled="isSavingPriority"
                size="default"
                rounded="lg"
                variant="tonal"
                class="task-page__chip"
                @change="emit('priority-change', $event)"
            />
        </div>
    </header>
</template>

<style scoped>
.task-page__topbar,
.task-page__header {
    --tp-ink: rgb(var(--v-theme-on-surface));
    --tp-ink-muted: #6b6960;
    --tp-line: #dad7ce;
    --tp-rust: #c1440e;
    --tp-teal: #205072;
}

.task-page__topbar {
    display: flex;
    align-items: center;
    min-height: 3.25rem;
    padding: 0.375rem 0.75rem;
    border-bottom: 0.0625rem solid var(--tp-line);
}

.task-page__actions {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.task-page__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1.5rem;
    padding: 1.25rem 0.5rem 1rem;
}

.task-page__identity {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    min-width: 0;
    flex: 1;
}

.editable-field--title {
    min-width: 0;
    max-width: 40rem;
}

.editable-field__display {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    min-width: 0;
}

.task-page__title {
    margin: 0;
    overflow: hidden;
    color: var(--tp-ink);
    font-size: 1.625rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.9rem;
    text-overflow: ellipsis;
    white-space: nowrap;
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
    color: var(--tp-ink-muted);
}

.editable-field__edit-btn:hover:deep(.v-icon) {
    color: var(--tp-ink);
}

.editable-field--title {
    min-width: 0;
    max-width: 40rem;
    flex: 1;
}

:deep(.editable-field--title .v-field) {
    --v-field-border-opacity: 1;

    min-height: 2.75rem;
    border-radius: 0.625rem;
    background: rgb(var(--v-theme-surface));

    outline: none !important;

    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease;
}

:deep(.editable-field--title input),
:deep(.editable-field--title input:focus),
:deep(.editable-field--title input:focus-visible) {
    outline: none !important;
    box-shadow: none !important;
}

:deep(.editable-field--title .v-field__outline) {
    color: rgb(var(--v-theme-outline, 225, 228, 232));
}

:deep(.editable-field--title .v-field__outline__start),
:deep(.editable-field--title .v-field__outline__end) {
    border-color: currentColor;
    opacity: 1;
}

:deep(.editable-field--title .v-field__outline__notch)::before,
:deep(.editable-field--title .v-field__outline__notch)::after {
    border-color: currentColor;
}

:deep(.editable-field--title .v-field:hover .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 0.55;
}

:deep(.editable-field--title .v-field--focused) {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

:deep(.editable-field--title .v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

:deep(.editable-field--title .v-field__input) {
    min-height: 2.75rem;
    padding-inline: 0.875rem;
    font-size: 1.125rem;
    font-weight: 600;
    line-height: 1.5rem;
    color: rgb(var(--v-theme-on-surface));
}

.task-page__badges {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.5rem;
    flex-wrap: wrap;
    padding-top: 0.3rem;
}

.task-page__chip :deep(.v-icon) {
    --v-icon-size-multiplier: 1;
    font-size: 1rem;
}

.task-page__overdue-flag {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.3rem 0.625rem;
    border-radius: 0.5rem;
    background: color-mix(in srgb, var(--tp-rust) 12%, transparent);
    color: var(--tp-rust);
    font-size: 0.75rem;
    font-weight: 600;
    user-select: none;
    -webkit-user-select: none;
}

.task-page__delete-item {
    color: rgb(var(--v-theme-error));
}

@media (max-width: 48rem) {
    .task-page__header {
        align-items: flex-start;
        flex-direction: column;
    }

    .task-page__badges {
        justify-content: flex-start;
        padding-top: 0;
    }
}
</style>
