`PendingTaskCard.vue` ```vue
<script setup>
import { computed, ref } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";

/** @typedef {import('@/types/task').TaskPriority} TaskPriority */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */

const props = defineProps({
    projects: {
        type: Array,
        default: () => [],
    },
});

const emit = defineEmits(["submit", "cancel"]);

const title = ref("");
const description = ref("");
const projectId = ref(null);
const priority = ref(/** @type {TaskPriority} */ ("medium"));
const tags = ref("");
const startDate = ref(null);
const dueDate = ref(null);

const priorityOptions = Object.keys(PRIORITY_COLORS).map((value) => ({
    title: value.charAt(0).toUpperCase() + value.slice(1),
    value,
}));

const canSubmit = computed(() => title.value.trim().length > 0);

function submit() {
    if (!canSubmit.value) return;

    /** @type {TaskCreate} */
    const task = {
        title: title.value.trim(),
        description: description.value.trim(),
        project_id: projectId.value,
        priority: priority.value,
        tags: tags.value
            .split(",")
            .map((tag) => tag.trim())
            .filter(Boolean)
            .join(","),
        start_date: startDate.value || null,
        due_date: dueDate.value || null,
        status: "open",
    };

    emit("submit", task);
}
</script>

<template>
    <v-card variant="outlined" rounded="lg" class="pending-task-card">
        <div class="status-rail bg-grey" />

        <div class="pa-4 pl-5">
            <div class="d-flex align-start ga-3 mb-3">
                <v-avatar
                    size="32"
                    color="grey"
                    variant="tonal"
                    class="flex-shrink-0"
                >
                    <v-icon icon="mdi-plus" size="16" />
                </v-avatar>

                <div class="flex-grow-1 min-width-0">
                    <v-text-field
                        v-model="title"
                        label="Title"
                        placeholder="What needs to be done?"
                        variant="outlined"
                        density="compact"
                        hide-details
                        autofocus
                    />

                    <v-textarea
                        v-model="description"
                        label="Description"
                        placeholder="Add a description..."
                        variant="outlined"
                        density="compact"
                        rows="2"
                        auto-grow
                        hide-details
                        class="mt-2"
                    />
                </div>

                <v-select
                    v-model="priority"
                    :items="priorityOptions"
                    label="Priority"
                    variant="outlined"
                    density="compact"
                    hide-details
                    class="priority-select flex-shrink-0"
                    style="width: 120px"
                />
            </div>

            <v-text-field
                v-model="tags"
                label="Tags"
                placeholder="bug, frontend, urgent"
                variant="outlined"
                density="compact"
                prepend-inner-icon="mdi-tag-outline"
                hide-details
                class="mb-3"
            />

            <v-divider class="mb-3" />

            <div class="task-meta">
                <v-select
                    v-model="projectId"
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

                <v-text-field
                    v-model="startDate"
                    type="date"
                    label="Start"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-inner-icon="mdi-calendar-start-outline"
                    class="meta-field"
                />

                <v-text-field
                    v-model="dueDate"
                    type="date"
                    label="Due"
                    variant="outlined"
                    density="compact"
                    hide-details
                    prepend-inner-icon="mdi-calendar-blank-outline"
                    class="meta-field"
                />
            </div>

            <div class="d-flex justify-end ga-2 mt-4">
                <v-btn variant="text" size="small" @click="emit('cancel')">
                    Cancel
                </v-btn>

                <v-btn
                    color="primary"
                    variant="flat"
                    size="small"
                    :disabled="!canSubmit"
                    prepend-icon="mdi-check"
                    @click="submit"
                >
                    Create task
                </v-btn>
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

.priority-select {
    min-width: 120px;
}

.task-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
}

.meta-field {
    min-width: 160px;
    flex: 1 1 160px;
}
</style>
