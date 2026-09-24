<script setup>
import { formatDate } from "@/utils/dateFormatters";

/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 * @typedef {import("@/types/task").TaskDraft} TaskDraft
 */

defineProps({
    task: {
        /**
         * @type {import("vue").PropType<TaskRead>}
         */
        type: Object,
        required: true,
    },
    draft: {
        /**
         * @type {import("vue").PropType<TaskDraft>}
         */
        type: Object,
        required: true,
    },
    isEditing: Boolean,
    isOverdue: Boolean,
    startDate: String,
    dueDate: String,
});

const emit = defineEmits([
    "edit",
    "save",
    "cancel",
    "update:startDate",
    "update:dueDate",
]);
</script>

<template>
    <section class="panel">
        <div class="panel__heading">
            <h2 class="panel__label">
                {{ isEditing ? "Edit details" : "Details" }}
            </h2>

            <div v-if="isEditing" class="panel__actions">
                <v-btn
                    icon="mdi-close"
                    size="small"
                    variant="text"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Cancel details edit"
                    @click="emit('cancel')"
                />

                <v-btn
                    icon="mdi-check"
                    size="small"
                    color="primary"
                    variant="tonal"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Save details"
                    @click="emit('save')"
                />
            </div>

            <v-btn
                v-else
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
            <div class="detail-editor__field">
                <label
                    class="detail-editor__field-label"
                    for="detail-start-date"
                    >Start</label
                >
                <v-text-field
                    id="detail-start-date"
                    :model-value="startDate"
                    @update:model-value="$emit('update:startDate', $event)"
                    type="date"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                />
            </div>

            <div class="detail-editor__field">
                <label class="detail-editor__field-label" for="detail-due-date"
                    >Due</label
                >
                <v-text-field
                    id="detail-due-date"
                    :model-value="dueDate"
                    @update:model-value="$emit('update:dueDate', $event)"
                    type="date"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                />
            </div>
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

.panel__actions {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.panel__actions .v-btn {
    border-radius: 999px;
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
    color: rgb(var(--v-theme-primary));
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

.detail-editor__field {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
}

.detail-editor__field-label {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.75rem;
    font-weight: 600;
}

.detail-editor :deep(.v-field) {
    --v-field-border-opacity: 1;
    min-height: 2.75rem;
    border-radius: 0.625rem;
    background: rgb(var(--v-theme-surface));
    outline: none;
}

.detail-editor :deep(.v-field__outline) {
    color: rgb(var(--v-theme-outline, 225, 228, 232));
    opacity: 1;
    transition: color 0.15s ease;
}

.detail-editor :deep(.v-field:hover .v-field__outline) {
    color: rgb(var(--v-theme-outline-variant, 165, 172, 182));
    opacity: 1;
}

.detail-editor :deep(.v-field:hover) {
    box-shadow: 0 0 0 0.0625rem
        rgba(var(--v-theme-outline-variant, 165, 172, 182), 0.5);
}

.detail-editor :deep(.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

.detail-editor :deep(.v-field--focused) {
    box-shadow: 0 0 0 0.0625rem rgba(var(--v-theme-primary), 0.15);
}

.detail-editor :deep(.v-field--focused:hover .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

.detail-editor :deep(.v-field--focused:hover) {
    box-shadow: 0 0 0 0.0625rem rgba(var(--v-theme-primary), 0.15);
}

.detail-editor :deep(.v-field__outline__start),
.detail-editor :deep(.v-field__outline__end) {
    border-color: currentColor;
    opacity: 1;
    transition: border-color 0.15s ease;
}

.detail-editor :deep(.v-field__outline__notch)::before,
.detail-editor :deep(.v-field__outline__notch)::after {
    border-color: currentColor;
    transition: border-color 0.15s ease;
}
</style>
