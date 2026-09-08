<script setup>
import { ref, watch } from "vue";

const props = defineProps({
    tags: {
        /** @type {import("vue").PropType<String[]>} */
        type: Array,
        default: () => [],
    },
    isEditing: Boolean,
});

const emit = defineEmits(["edit", "cancel", "save"]);

const tagsInput = ref(props.tags.join(", "));

watch(
    () => props.isEditing,
    (isEditing) => {
        if (isEditing) {
            tagsInput.value = props.tags.join(", ");
        }
    }
);

function handleSave() {
    const parsed = tagsInput.value
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean);
    emit("save", parsed);
}
</script>

<template>
    <section class="panel">
        <div class="panel__heading">
            <h2 class="panel__label">
                {{ isEditing ? "Edit tags" : "Tags" }}
            </h2>

            <div v-if="isEditing" class="panel__actions">
                <v-btn
                    icon="mdi-close"
                    size="small"
                    variant="text"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Cancel tags edit"
                    @click="emit('cancel')"
                />

                <v-btn
                    icon="mdi-check"
                    size="small"
                    color="primary"
                    variant="tonal"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Save tags"
                    @click="handleSave"
                />
            </div>

            <v-btn
                v-else
                class="panel__edit-btn"
                icon="mdi-pencil-outline"
                size="x-small"
                variant="text"
                density="comfortable"
                aria-label="Edit tags"
                @click="emit('edit')"
            />
        </div>

        <div v-if="isEditing" class="tag-editor">
            <v-text-field
                v-model="tagsInput"
                placeholder="design, backend, urgent"
                variant="outlined"
                density="comfortable"
                hide-details
                @keydown.enter.prevent="handleSave"
                @keydown.esc.prevent="emit('cancel')"
            />
        </div>

        <div v-else-if="tags.length" class="tag-list">
            <v-chip
                v-for="tag in tags"
                :key="tag"
                size="small"
                variant="flat"
                class="tag-chip"
                ripple
            >
                {{ tag }}
            </v-chip>
        </div>

        <button v-else type="button" class="panel__empty" @click="emit('edit')">
            <v-icon icon="mdi-tag-plus-outline" size="16" />
            <span>No tags yet — click to add some</span>
        </button>
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
    border-radius: 9999px;
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

.panel__empty {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    width: 100%;
    padding: 0.75rem;
    border: 0.0625rem dashed rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.625rem;
    background: transparent;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition:
        border-color 0.12s ease,
        color 0.12s ease;
}

.panel__empty:hover {
    border-color: rgba(25, 118, 210, 0.35);
    color: #1976d2;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.375rem;
}

.tag-chip {
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248)) !important;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103)) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: normal !important;
    transition:
        background-color 0.12s ease,
        color 0.12s ease;
}

.tag-chip:deep(.v-chip__content) {
    user-select: none;
    -webkit-user-select: none;
}

.tag-chip:hover {
    background: color-mix(
        in srgb,
        #1976d2 10%,
        rgb(var(--v-theme-grey-lighten-4, 245, 246, 248))
    ) !important;
    color: #1976d2 !important;
}

.tag-editor {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.tag-editor :deep(.v-field) {
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

.tag-editor :deep(.v-field__outline) {
    color: rgb(var(--v-theme-outline-variant, 234, 236, 240));
    transition:
        color 0.15s ease,
        opacity 0.15s ease;
}

.tag-editor :deep(.v-field:hover .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 0.55;
}

.tag-editor :deep(.v-field:hover) {
    box-shadow: 0 0 0 0.125rem rgba(var(--v-theme-primary), 0.06);
}

.tag-editor :deep(.v-field--focused) {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.12);
}

.tag-editor :deep(.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

.tag-editor :deep(.v-field__outline__start),
.tag-editor :deep(.v-field__outline__end) {
    border-color: currentColor;
    opacity: 1;
    transition: border-color 0.15s ease;
}

.tag-editor :deep(.v-field__outline__notch)::before,
.tag-editor :deep(.v-field__outline__notch)::after {
    border-color: currentColor;
    transition: border-color 0.15s ease;
}
</style>
