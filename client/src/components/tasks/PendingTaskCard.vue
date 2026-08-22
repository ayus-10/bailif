<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import { computed, ref } from "vue";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

/** @typedef {import('@/types/task').TaskPriority} TaskPriority */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */

const props = defineProps({
    projects: {
        type: Array,
        default: () => [],
    },
    parentId: {
        type: String,
        default: null,
    },
});

const emit = defineEmits(["submit", "cancel"]);

const emptyForm = {
    title: "",
    description: "",
    projectId: null,
    priority: /** @type {TaskPriority} */ ("medium"),
    tags: "",
    startDate: null,
    dueDate: null,
};

const form = ref({ ...emptyForm });

/** @type {{ title: string, value: TaskPriority }[]} */
const priorityOptions = [
    { title: "Low", value: "low" },
    { title: "Medium", value: "medium" },
    { title: "High", value: "high" },
];

const canSubmit = computed(() => form.value.title.trim().length > 0);

function submit() {
    if (!canSubmit.value) return;

    /** @type {TaskCreate} */
    const task = {
        title: form.value.title.trim(),
        description: form.value.description.trim(),
        project_id: form.value.projectId,
        parent_id: props.parentId,
        priority: form.value.priority,
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
        <div class="pa-4 pl-5">
            <div class="d-flex justify-end ga-1 mb-2">
                <v-btn
                    icon="mdi-check"
                    size="small"
                    variant="text"
                    color="primary"
                    :disabled="!canSubmit"
                    @click="submit"
                >
                    <v-icon size="20">mdi-check</v-icon>

                    <v-tooltip activator="parent" location="top">
                        Save
                    </v-tooltip>
                </v-btn>

                <v-btn
                    icon="mdi-close"
                    size="small"
                    variant="text"
                    @click="cancel"
                >
                    <v-icon size="20">mdi-close</v-icon>

                    <v-tooltip activator="parent" location="top">
                        Cancel
                    </v-tooltip>
                </v-btn>
            </div>

            <v-text-field
                v-model="form.title"
                label="Title"
                placeholder="What needs to be done?"
                variant="outlined"
                density="compact"
                hide-details
                autofocus
            />

            <QuillEditor
                v-model:content="form.description"
                content-type="html"
                theme="snow"
                placeholder="Add a description..."
                toolbar="minimal"
                class="mt-3"
            />

            <div class="d-flex ga-3 mt-3">
                <v-select
                    v-model="form.priority"
                    :items="priorityOptions"
                    label="Priority"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="meta-field"
                />

                <v-select
                    v-model="form.projectId"
                    :items="projects"
                    item-title="name"
                    item-value="id"
                    label="Project"
                    placeholder="Project"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-inner-icon="mdi-folder-outline"
                    class="meta-field"
                />
            </div>

            <v-text-field
                v-model="form.tags"
                label="Tags"
                placeholder="bug, frontend, urgent"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-tag-outline"
                hide-details
                class="mt-3"
            />

            <div class="d-flex ga-3 mt-3">
                <v-text-field
                    v-model="form.startDate"
                    type="date"
                    label="Start"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-inner-icon="mdi-calendar-start-outline"
                    class="meta-field"
                />

                <v-text-field
                    v-model="form.dueDate"
                    type="date"
                    label="Due"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-inner-icon="mdi-calendar-blank-outline"
                    class="meta-field"
                />
            </div>
        </div>
    </v-card>
</template>

<style scoped>
.pending-task-card {
    position: relative;
    overflow: hidden;
}

.status-rail {
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
}

.meta-field {
    min-width: 160px;
    flex: 1 1 160px;
}
</style>
