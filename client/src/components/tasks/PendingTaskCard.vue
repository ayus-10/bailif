<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import { computed, ref } from "vue";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

/** @typedef {import('@/types/task').TaskPriority} TaskPriority */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */

const props = defineProps({
    projectId: {
        type: String,
    },
    parentId: {
        type: String,
        default: null,
    },
    taskboardId: {
        type: [String, null],
        default: null,
    },
});

const emit = defineEmits(["submit", "cancel"]);

const COMPOSER_CONFIG = {
    title: {
        label: "Task title",
        placeholder: "What needs to be done?",
    },
    description: {
        placeholder: "Add a description...",
        toolbar: "minimal",
    },
    priority: {
        label: "Priority",
    },
    tags: {
        label: "Tags",
        placeholder: "bug, frontend, urgent",
        icon: "mdi-tag-outline",
    },
    startDate: {
        label: "Start date",
        icon: "mdi-calendar-start-outline",
    },
    dueDate: {
        label: "Due date",
        icon: "mdi-calendar-end-outline",
    },
    actions: {
        saveLabel: "Save task",
        cancelLabel: "Cancel",
        saveIcon: "mdi-check",
        cancelIcon: "mdi-close",
    },
};

const priorityOptions = [
    { title: "Low", value: "low" },
    { title: "Medium", value: "medium" },
    { title: "High", value: "high" },
];

const emptyForm = {
    title: "",
    description: "",
    priority: /** @type {TaskPriority} */ ("medium"),
    tags: "",
    startDate: null,
    dueDate: null,
};

const form = ref({ ...emptyForm });

const canSubmit = computed(() => form.value.title.trim().length > 0);

function submit() {
    if (!canSubmit.value) return;

    /** @type {TaskCreate} */
    const task = {
        title: form.value.title.trim(),
        description: form.value.description.trim(),
        project_id: String(props.projectId), // TODO: fix this, someday
        parent_id: props.parentId,
        priority: form.value.priority,
        taskboard_id: props.taskboardId,
        tags: form.value.tags
            .split(",")
            .map((tag) => tag.trim())
            .filter(Boolean)
            .join(","),
        start_date: form.value.startDate || null,
        due_date: form.value.dueDate || null,
        status: "open",
    };

    emit("submit", task);
}

function cancel() {
    emit("cancel");
    form.value = { ...emptyForm };
}
</script>

<template>
    <v-card rounded="lg" border elevation="0" class="pending-task-card">
        <div class="pending-task-card__header">
            <span class="pending-task-card__eyebrow"> New task </span>

            <div class="pending-task-card__actions">
                <v-btn
                    :icon="COMPOSER_CONFIG.actions.cancelIcon"
                    :aria-label="COMPOSER_CONFIG.actions.cancelLabel"
                    size="small"
                    variant="text"
                    density="comfortable"
                    @click="cancel"
                >
                    <v-icon
                        :icon="COMPOSER_CONFIG.actions.cancelIcon"
                        size="1.125rem"
                    />

                    <v-tooltip activator="parent" location="top">
                        {{ COMPOSER_CONFIG.actions.cancelLabel }}
                    </v-tooltip>
                </v-btn>

                <v-btn
                    :icon="COMPOSER_CONFIG.actions.saveIcon"
                    :aria-label="COMPOSER_CONFIG.actions.saveLabel"
                    size="small"
                    variant="text"
                    color="primary"
                    density="comfortable"
                    :disabled="!canSubmit"
                    @click="submit"
                >
                    <v-icon
                        :icon="COMPOSER_CONFIG.actions.saveIcon"
                        size="1.125rem"
                    />

                    <v-tooltip activator="parent" location="top">
                        {{ COMPOSER_CONFIG.actions.saveLabel }}
                    </v-tooltip>
                </v-btn>
            </div>
        </div>

        <div class="pending-task-card__content">
            <v-text-field
                v-model="form.title"
                :label="COMPOSER_CONFIG.title.label"
                :placeholder="COMPOSER_CONFIG.title.placeholder"
                variant="outlined"
                density="comfortable"
                hide-details
                autofocus
                class="task-title-field"
            />

            <QuillEditor
                v-model:content="form.description"
                content-type="html"
                theme="snow"
                :placeholder="COMPOSER_CONFIG.description.placeholder"
                :toolbar="COMPOSER_CONFIG.description.toolbar"
                class="task-description-editor"
            />

            <div class="task-meta">
                <v-select
                    v-model="form.priority"
                    :items="priorityOptions"
                    :label="COMPOSER_CONFIG.priority.label"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="task-meta__field"
                />

                <v-text-field
                    v-model="form.tags"
                    :label="COMPOSER_CONFIG.tags.label"
                    :placeholder="COMPOSER_CONFIG.tags.placeholder"
                    :prepend-inner-icon="COMPOSER_CONFIG.tags.icon"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="task-meta__field"
                />
            </div>

            <div class="task-dates">
                <v-text-field
                    v-model="form.startDate"
                    :label="COMPOSER_CONFIG.startDate.label"
                    :prepend-inner-icon="COMPOSER_CONFIG.startDate.icon"
                    type="date"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="task-dates__field"
                />

                <v-text-field
                    v-model="form.dueDate"
                    :label="COMPOSER_CONFIG.dueDate.label"
                    :prepend-inner-icon="COMPOSER_CONFIG.dueDate.icon"
                    type="date"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="task-dates__field"
                />
            </div>
        </div>
    </v-card>
</template>

<style scoped>
.pending-task-card {
    position: relative;
    min-width: 0;
    overflow: hidden;
}

.pending-task-card__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.75rem 0.875rem;
    border-bottom: 1px solid color-mix(in srgb, currentColor 10%, transparent);
}

.pending-task-card__eyebrow {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.pending-task-card__actions {
    display: flex;
    align-items: center;
    gap: 0.125rem;
    flex: 0 0 auto;
}

.pending-task-card__content {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0.875rem;
}

.task-title-field {
    flex: 0 0 auto;
}

.task-description-editor {
    min-width: 0;
}

.task-meta {
    display: flex;
    gap: 0.75rem;
    min-width: 0;
}

.task-meta__field {
    min-width: 0;
    flex: 1 1 0;
}

.task-dates {
    display: flex;
    gap: 0.75rem;
    min-width: 0;
}

.task-dates__field {
    min-width: 0;
    flex: 1 1 0;
}

:deep(.task-description-editor .ql-toolbar) {
    border: 0;
    border-bottom: 1px solid color-mix(in srgb, currentColor 10%, transparent);
    padding: 0.375rem 0.5rem;
}

:deep(.task-description-editor .ql-container) {
    border: 0;
    min-height: 5.5rem;
}

:deep(.task-description-editor .ql-editor) {
    min-height: 5.5rem;
    padding: 0.625rem 0.5rem;
    font-size: 0.8125rem;
    line-height: 1.5;
}

:deep(.task-description-editor .ql-editor.ql-blank::before) {
    left: 0.5rem;
    right: 0.5rem;
    font-style: normal;
}
</style>
