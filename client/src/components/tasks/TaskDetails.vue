<script setup>
import { formatDate } from "@/utils/taskFormatters";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskDraft} TaskDraft */

defineProps({
    task: {
        /** @type {import("vue").PropType<TaskRead>} */
        type: Object,
        required: true,
    },
    draft: {
        /** @type {import("vue").PropType<TaskDraft>} */
        type: Object,
        required: true,
    },
    isEditing: Boolean,
    isOverdue: Boolean,
    startDate: String,
    dueDate: String,
});

const emit = defineEmits(["edit"]);
</script>

<template>
    <section class="panel" :class="{ 'panel--editing': isEditing }">
        <div class="panel__heading">
            <h2 class="panel__label">Details</h2>
            <v-btn
                v-if="!isEditing"
                class="panel__edit-btn"
                icon="mdi-pencil-outline"
                size="x-small"
                variant="text"
                density="comfortable"
                aria-label="Edit details"
                @click="emit('edit')"
            />
        </div>

        <dl v-if="!isEditing" class="detail-list">
            <div class="detail-list__row">
                <dt>Project</dt>
                <dd>
                    {{ task.project?.name ?? "—" }}
                </dd>
            </div>
            <div class="detail-list__row">
                <dt>Start</dt>
                <dd>
                    {{ formatDate(task.start_date) ?? "—" }}
                </dd>
            </div>
            <div class="detail-list__row">
                <dt>Due</dt>
                <dd class="detail-list__value" :class="{ overdue: isOverdue }">
                    {{ formatDate(task.due_date) ?? "—" }}
                </dd>
            </div>
        </dl>

        <div v-else class="detail-editor">
            <v-text-field
                :model-value="startDate"
                label="Start"
                type="date"
                variant="outlined"
                density="compact"
                hide-details
            />
            <v-text-field
                :model-value="dueDate"
                label="Due"
                type="date"
                variant="outlined"
                density="compact"
                hide-details
            />
        </div>
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

.panel--editing {
    border-color: rgba(25, 118, 210, 0.35);
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    min-height: 1.5rem;
}

.panel__label {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
}

.panel__edit-btn {
    opacity: 0;
    transition: opacity 0.12s ease;
}

.panel:hover .panel__edit-btn,
.panel:focus-within .panel__edit-btn {
    opacity: 1;
}

.panel__edit-btn:deep(.v-icon) {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
}

.panel__edit-btn:hover:deep(.v-icon) {
    color: #1976d2;
}

.detail-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin: 0;
}

.detail-list__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    min-height: 1.5rem;
}

.detail-list__row dt {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    font-weight: 600;
}

.detail-list__row dd {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.8125rem;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    text-align: right;
}

.detail-list__value.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 700;
}

.detail-editor {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.detail-editor :deep(.v-field--variant-outlined .v-field__outline) {
    color: rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.detail-editor
    :deep(.v-field--variant-outlined.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-on-surface));
}
</style>
