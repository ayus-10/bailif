<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import SubtaskPanel from "@/components/tasks/SubtaskPanel.vue";
import TaskDescription from "@/components/tasks/TaskDescription.vue";
import TaskDetails from "@/components/tasks/TaskDetails.vue";
import TaskPageHeader from "@/components/tasks/TaskPageHeader.vue";
import TaskTags from "@/components/tasks/TaskTags.vue";
import { useTaskEditor } from "@/composables/useTaskEditor";
import { useTasksStore } from "@/stores/tasks.store";
import { parseTags } from "@/utils/taskFormatters";

const route = useRoute();
const router = useRouter();

const currentTaskId = computed(() => {
    const id = route.params.id;
    return Array.isArray(id) ? id[0] : id;
});

const projectId = ref(localStorage.getItem("project_id") ?? ""); // TODO: replace with session

const tasksStore = useTasksStore();

onMounted(() => {
    tasksStore.get(currentTaskId.value);
});

const currentTask = computed(() => tasksStore.currentTask);

const tags = computed(() =>
    currentTask.value ? parseTags(currentTask.value.tags) : []
);

const {
    editMode,
    draft,

    isSaving,
    hasPendingChanges,

    isEditingTitle,
    isEditingDescription,
    isEditingDetails,

    selectedStatus,
    selectedPriority,

    isSavingStatus,
    isSavingPriority,

    isOverdue,

    startDate,
    dueDate,

    beginEdit,
    cancelChanges,
    saveChanges,

    onStatusChange,
    onPriorityChange,
} = useTaskEditor(currentTask, currentTaskId.value);
</script>

<template>
    <div v-if="currentTask" class="task-page" @contextmenu.prevent>
        <TaskPageHeader
            :task="currentTask"
            :edit-mode="editMode"
            :draft="draft"
            :selected-status="selectedStatus"
            :selected-priority="selectedPriority"
            :is-saving="isSaving"
            :is-saving-status="isSavingStatus"
            :is-saving-priority="isSavingPriority"
            :has-pending-changes="hasPendingChanges"
            :is-overdue="isOverdue"
            :is-editing-title="isEditingTitle"
            @back="router.back()"
            @edit="beginEdit"
            @cancel="cancelChanges"
            @save="saveChanges"
            @status-change="onStatusChange"
            @priority-change="onPriorityChange"
        />

        <div class="task-page__body">
            <main class="task-page__main">
                <TaskDescription
                    :task="currentTask"
                    :draft="draft"
                    :is-editing="isEditingDescription"
                    @edit="beginEdit('description')"
                />
            </main>

            <aside class="task-page__sidebar">
                <TaskDetails
                    :task="currentTask"
                    :draft="draft"
                    :is-editing="isEditingDetails"
                    :is-overdue="isOverdue"
                    :start-date="startDate"
                    :due-date="dueDate"
                    @edit="beginEdit('details')"
                />

                <TaskTags :tags="tags" />

                <SubtaskPanel
                    :task-id="currentTaskId"
                    :project-id="projectId"
                />
            </aside>
        </div>
    </div>
</template>

<style scoped>
.task-page {
    margin: 0 auto;
    padding: 1.25rem 1.25rem 3.5rem;
    color: rgb(var(--v-theme-on-surface));
    user-select: none;
}

.task-page :deep(input),
.task-page :deep(textarea),
.task-page :deep(.ql-editor) {
    user-select: text;
}

.task-page__body {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 17.5rem;
    align-items: start;
    gap: 1.5rem;
}

.task-page__main {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    min-width: 0;
}

.task-page__sidebar {
    position: sticky;
    top: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

@media (max-width: 47.5rem) {
    .task-page {
        padding: 1rem 1rem 2.5rem;
    }

    .task-page__body {
        grid-template-columns: 1fr;
    }

    .task-page__sidebar {
        position: static;
    }
}
</style>
