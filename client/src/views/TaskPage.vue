<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, reactive, ref, watch } from "vue";
import EditableVChip from "@/components/common/EditableVChip.vue";
import SubtaskPanel from "@/components/tasks/SubtaskPanel.vue";
import { STATUS_META, TASK_PRIORITIES } from "@/constants/taskMeta";
import { PRIORITY_COLORS, PRIORITY_ICONS } from "@/constants/tasks";
import { isHtmlEmpty } from "@/utils/htmlFormatters";
import { formatDate, isTaskOverdue, parseTags } from "@/utils/taskFormatters";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "@/components/quill-editor.css";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskDraft} TaskDraft */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {TaskRead["status"]} TaskStatus */
/** @typedef {TaskRead["priority"]} TaskPriority */
/** @typedef {"title" | "description" | "details" | "none"} EditMode */

const route = useRoute();
const router = useRouter();
const tasksStore = useTasksStore();

const taskId = String(route.params.id);
const projectId = ref(localStorage.getItem("project_id") ?? ""); // TODO: replace with session

onMounted(() => {
    tasksStore.get(taskId);
});

const task = computed(() => tasksStore.currentTask);

const editMode = ref(/** @type {EditMode} */ ("none"));
const hasPendingChanges = ref(false);
const isSaving = ref(false);

const isEditingTitle = computed(() => editMode.value === "title");
const isEditingDescription = computed(() => editMode.value === "description");
const isEditingDetails = computed(() => editMode.value === "details");

const draft = reactive(getTaskDraft(null));
const originalDraft = reactive(getTaskDraft(null));

const selectedStatus = ref(task.value?.status ?? "");
const selectedPriority = ref(task.value?.priority ?? "");

watch(
    draft,
    () => {
        if (editMode.value === "none") {
            hasPendingChanges.value = false;
            return;
        }

        hasPendingChanges.value =
            JSON.stringify(draft) !== JSON.stringify(originalDraft);
    },
    { deep: true }
);

watch(
    task,
    (newTask) => {
        if (!newTask) return;

        selectedStatus.value = newTask.status;
        selectedPriority.value = newTask.priority;

        // Don't overwrite local edits while the user is editing.
        if (editMode.value === "none") {
            syncDraftFromTask();
        }
    },
    { immediate: true }
);

const statusOptions = computed(() =>
    Object.entries(STATUS_META).map(([value, meta]) => ({
        value,
        label: meta.label,
        color: meta.color,
        icon: meta.icon,
    }))
);

const priorityOptions = computed(() =>
    TASK_PRIORITIES.map((value) => ({
        value,
        label: value.toUpperCase(),
        color: PRIORITY_COLORS[value],
        icon: PRIORITY_ICONS[value],
    }))
);

const isSavingStatus = ref(false);
const isSavingPriority = ref(false);

const isOverdue = computed(() =>
    task.value ? isTaskOverdue(task.value) : false
);

const tags = computed(() => (task.value ? parseTags(task.value.tags) : []));

const toolbarOptions = [
    ["bold", "italic", "underline"],
    [{ list: "ordered" }, { list: "bullet" }, { list: "check" }],
];

const startDate = computed({
    get() {
        return draft.start_date
            ? new Date(draft.start_date).toISOString().slice(0, 10)
            : "";
    },
    set(value) {
        draft.start_date = value;
    },
});

const dueDate = computed({
    get() {
        return draft.due_date
            ? new Date(draft.due_date).toISOString().slice(0, 10)
            : "";
    },
    set(value) {
        draft.due_date = value;
    },
});

/**
 * @param {TaskRead | null | undefined} source
 * @returns {TaskDraft}
 */
function getTaskDraft(source) {
    return {
        project_id: source?.project?.id ?? null,
        title: source?.title ?? "",
        description: source?.description ?? "",
        status: source?.status ?? null,
        priority: source?.priority ?? null,
        start_date: source?.start_date ?? null,
        due_date: source?.due_date ?? null,
    };
}

/**
 * @param {TaskDraft} target
 * @param {TaskDraft} source
 */
function copyDraftValues(target, source) {
    Object.assign(target, source);
}

function syncDraftFromTask() {
    if (!task.value) return;

    const values = getTaskDraft(task.value);
    copyDraftValues(draft, values);
    copyDraftValues(originalDraft, values);

    hasPendingChanges.value = false;
}

/** @param {EditMode} mode */
function beginEdit(mode) {
    if (!task.value) return;

    if (editMode.value === "none") {
        syncDraftFromTask();
    }

    editMode.value = mode;
}

function cancelChanges() {
    copyDraftValues(draft, originalDraft);
    hasPendingChanges.value = false;
    editMode.value = "none";
}

async function saveChanges() {
    if (!task.value || !hasPendingChanges.value) {
        editMode.value = "none";
        return;
    }

    isSaving.value = true;

    try {
        const payload = buildUpdatePayload(draft, originalDraft);

        await tasksStore.update(taskId, payload);

        copyDraftValues(originalDraft, draft);

        hasPendingChanges.value = false;
        editMode.value = "none";
    } finally {
        isSaving.value = false;
    }
}

/**
 * @param {TaskDraft} draft
 * @param {TaskDraft} originalDraft
 * @returns {Partial<TaskCreate>}
 */
function buildUpdatePayload(draft, originalDraft) {
    /** @type {Partial<TaskDraft>} */
    const payload = {};
    const draftFields = /** @type {(keyof TaskDraft)[]} */ (Object.keys(draft));

    for (const field of draftFields) {
        if (draft[field] !== originalDraft[field]) {
            Object.assign(payload, { [field]: draft[field] });
        }
    }

    if (payload.status === null) delete payload.status;
    if (payload.priority === null) delete payload.priority;

    return /** @type {Partial<TaskCreate>} */ (payload);
}

/**
 * @template {"status" | "priority"} F
 * @param {F} field
 * @param {{ value: string }} item
 * @param {import('vue').Ref<string>} localRef
 * @param {import('vue').Ref<boolean>} savingRef
 */
async function updateTaskField(field, item, localRef, savingRef) {
    if (!task.value) return;

    const previousValue = task.value[field];
    savingRef.value = true;

    try {
        await tasksStore.update(taskId, { [field]: item.value });
    } catch (error) {
        localRef.value = previousValue;
        throw error;
    } finally {
        savingRef.value = false;
    }
}

/** @param {{ value: TaskStatus }} item */
function onStatusChange(item) {
    return updateTaskField("status", item, selectedStatus, isSavingStatus);
}

/** @param {{ value: TaskPriority }} item */
function onPriorityChange(item) {
    return updateTaskField(
        "priority",
        item,
        selectedPriority,
        isSavingPriority
    );
}
</script>

<template>
    <div v-if="task" class="task-page" @contextmenu.prevent>
        <div class="task-page__topbar">
            <v-btn
                class="task-page__back"
                icon="mdi-arrow-left"
                variant="text"
                density="comfortable"
                aria-label="Go back"
                @click="router.back()"
            />

            <v-spacer />

            <div v-if="editMode !== 'none'" class="task-page__actions">
                <v-btn
                    variant="text"
                    density="comfortable"
                    :disabled="isSaving"
                    @click="cancelChanges"
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
                    @click="saveChanges"
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
                    @keydown.escape="cancelChanges"
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
                        @click="beginEdit('title')"
                    />
                </div>
            </div>

            <div class="task-page__badges">
                <EditableVChip
                    v-model="selectedStatus"
                    :items="statusOptions"
                    :disabled="isSavingStatus"
                    size="small"
                    variant="tonal"
                    @change="onStatusChange"
                />

                <EditableVChip
                    v-model="selectedPriority"
                    :items="priorityOptions"
                    :disabled="isSavingPriority"
                    size="small"
                    variant="tonal"
                    @change="onPriorityChange"
                />

                <span v-if="isOverdue" class="task-page__overdue-flag">
                    <v-icon icon="mdi-calendar-alert" size="15" />
                    Overdue
                </span>
            </div>
        </header>

        <div class="task-page__body">
            <main class="task-page__main">
                <section class="panel">
                    <div class="panel__heading">
                        <h2 class="panel__label">Description</h2>

                        <v-btn
                            v-if="!isEditingDescription"
                            class="panel__edit-btn"
                            icon="mdi-pencil-outline"
                            size="x-small"
                            variant="text"
                            density="comfortable"
                            aria-label="Edit description"
                            @click="beginEdit('description')"
                        />
                    </div>

                    <div v-if="isEditingDescription" class="description-editor">
                        <QuillEditor
                            v-model:content="draft.description"
                            content-type="html"
                            theme="snow"
                            placeholder="Add a description..."
                            :toolbar="toolbarOptions"
                        />
                    </div>

                    <div
                        v-else-if="!isHtmlEmpty(task.description)"
                        v-html="task.description"
                        class="prose"
                        @click="beginEdit('description')"
                    ></div>

                    <p
                        v-else
                        class="panel__empty"
                        @click="beginEdit('description')"
                    >
                        No description yet.
                    </p>
                </section>
            </main>

            <aside class="task-page__sidebar">
                <section
                    class="panel"
                    :class="{
                        'panel--editing': isEditingDetails,
                    }"
                >
                    <div class="panel__heading">
                        <h2 class="panel__label">Details</h2>

                        <v-btn
                            v-if="!isEditingDetails"
                            class="panel__edit-btn"
                            icon="mdi-pencil-outline"
                            size="x-small"
                            variant="text"
                            density="comfortable"
                            aria-label="Edit details"
                            @click="beginEdit('details')"
                        />
                    </div>

                    <dl v-if="!isEditingDetails" class="detail-list">
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
                            <dd :class="{ overdue: isOverdue }">
                                {{ formatDate(task.due_date) ?? "—" }}
                            </dd>
                        </div>
                    </dl>

                    <div v-else class="detail-editor">
                        <v-text-field
                            v-model="startDate"
                            label="Start"
                            type="date"
                            variant="outlined"
                            density="compact"
                            hide-details
                        />

                        <v-text-field
                            v-model="dueDate"
                            label="Due"
                            type="date"
                            variant="outlined"
                            density="compact"
                            hide-details
                        />
                    </div>
                </section>

                <section v-if="tags.length" class="panel">
                    <h2 class="panel__label">Tags</h2>

                    <div class="tag-list">
                        <v-chip
                            v-for="tag in tags"
                            :key="tag"
                            size="small"
                            variant="tonal"
                        >
                            {{ tag }}
                        </v-chip>
                    </div>
                </section>

                <SubtaskPanel :task-id="taskId" :project-id="projectId" />
            </aside>
        </div>
    </div>
</template>

<style scoped>
.task-page {
    margin: 0 auto;
    padding: 20px 20px 56px;
    color: rgb(var(--v-theme-on-surface));
    user-select: none;
}

.task-page :deep(input),
.task-page :deep(textarea),
.task-page :deep(.ql-editor) {
    user-select: text;
}

.task-page__topbar {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 40px;
}

.task-page__back {
    flex: 0 0 auto;
}

.task-page__actions {
    display: flex;
    align-items: center;
    gap: 4px;
}

.task-page__header {
    padding: 18px 0 24px;
    margin-bottom: 24px;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.task-page__title {
    min-width: 0;
    margin: 0;
    font-size: 1.75rem;
    font-weight: 600;
    line-height: 1.25;
    letter-spacing: -0.015em;
}

.task-page__badges {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 12px;
}

.task-page__overdue-flag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    min-height: 28px;
    padding: 0 8px;
    border-radius: 6px;
    background: rgba(var(--v-theme-error), 0.08);
    color: rgb(var(--v-theme-error));
    font-size: 0.75rem;
    font-weight: 600;
}

.task-page__body {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 280px;
    align-items: start;
    gap: 24px;
}

.task-page__main {
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-width: 0;
}

.task-page__sidebar {
    position: sticky;
    top: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.panel {
    padding: 16px 18px;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-radius: 10px;
    background: rgb(var(--v-theme-surface));
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.035);
    transition:
        border-color 140ms ease,
        box-shadow 140ms ease;
}

.panel:hover {
    border-color: rgba(var(--v-theme-on-surface), 0.12);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.panel--editing {
    box-shadow: 0 2px 4px rgba(var(--v-theme-primary), 0.06);
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
}

.panel__label {
    margin: 0;
    color: rgba(var(--v-theme-on-surface), 0.55);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    line-height: 1.4;
    text-transform: uppercase;
}

.panel__edit-btn,
.editable-field__edit-btn {
    opacity: 0;
    transition:
        opacity 120ms ease,
        background-color 120ms ease,
        color 120ms ease;
}

.panel:hover .panel__edit-btn,
.panel__edit-btn:focus-visible,
.editable-field:hover .editable-field__edit-btn,
.editable-field__edit-btn:focus-visible {
    opacity: 1;
}

.panel__edit-btn:focus-visible,
.editable-field__edit-btn:focus-visible,
.task-page__back:focus-visible {
    outline: 2px solid rgb(var(--v-theme-primary));
    outline-offset: 2px;
}

.panel__empty {
    margin: 0;
    color: rgba(var(--v-theme-on-surface), 0.5);
    user-select: text;
    font-size: 0.875rem;
    font-style: italic;
}

.editable-field {
    position: relative;
    min-width: 0;
}

.editable-field__display {
    display: flex;
    align-items: center;
    min-width: 0;
    gap: 10px;
}

.editable-field--editing {
    max-width: 700px;
}

.prose {
    color: rgba(var(--v-theme-on-surface), 0.87);
    font-size: 0.9375rem;
    line-height: 1.7;
    user-select: text;
}

.prose p {
    margin: 0 0 1em;
    white-space: pre-wrap;
}

.prose p:last-child {
    margin-bottom: 0;
}

.description-editor {
    width: 100%;
    overflow: hidden;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
    border-radius: 8px;
}

.detail-list {
    margin: 0;
}

.detail-list__row {
    display: grid;
    grid-template-columns: 88px minmax(0, 1fr);
    align-items: center;
    gap: 12px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
    font-size: 0.8125rem;
}

.detail-list__row:last-child {
    border-bottom: none;
}

.detail-list__row dt {
    min-width: 0;
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.detail-list__row dd {
    min-width: 0;
    margin: 0;
    overflow: hidden;
    color: rgba(var(--v-theme-on-surface), 0.88);
    font-weight: 500;
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
}

.detail-list__row dd.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.detail-editor {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.task-page :deep(.v-ripple__container) {
    display: none;
}

.task-page :deep(.v-btn) {
    transition:
        background-color 120ms ease,
        color 120ms ease,
        border-color 120ms ease;
}

.task-page :deep(.v-btn),
.task-page :deep(.v-chip),
.task-page :deep(.v-icon),
.task-page :deep(.v-field__label),
.task-page :deep(.v-field__append-inner),
.task-page :deep(.v-field__prepend-inner) {
    user-select: none;
}

@media (max-width: 760px) {
    .task-page {
        padding: 16px 16px 40px;
    }

    .task-page__body {
        grid-template-columns: 1fr;
    }

    .task-page__sidebar {
        position: static;
    }

    .task-page__title {
        font-size: 1.5rem;
    }
}
</style>
