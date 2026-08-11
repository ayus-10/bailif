<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { PRIORITY_COLORS } from "@/constants/tasks";
import {
    STATUS_META,
    TYPE_ICONS,
    TYPE_LABELS,
    FALLBACK_TYPE_ICON,
} from "@/constants/taskMeta";
import {
    formatDate,
    formatDuration,
    isTaskOverdue,
    parseTags,
} from "@/utils/taskFormatters";
import { htmlToText } from "@/utils/htmlFormatters";
import { useTasksStore } from "@/stores/tasks.store";
import EditableVChip from "@/components/layout/EditableVChip.vue";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {TaskRead["status"]} TaskStatus */
/** @typedef {TaskRead["priority"]} TaskPriority */
/** @typedef {"title" | "description" | "details" | "none"} EditMode */

/**
 * @typedef {Object} TaskDraft
 * @property {string} title
 * @property {string} description
 * @property {TaskStatus | ""} status
 * @property {TaskPriority | ""} priority
 * @property {string} start_date
 * @property {string} due_date
 * @property {number | null} estimated_duration_minutes
 */

// Icons aren't part of PRIORITY_COLORS today, so we map them here. Add a
// key whenever a new priority value is introduced; unmapped values fall
// back to a generic flag icon.
/** @type {Record<string, string>} */
const PRIORITY_ICONS = {
    low: "mdi-arrow-down",
    medium: "mdi-minus",
    high: "mdi-arrow-up",
    urgent: "mdi-alert",
};
const FALLBACK_PRIORITY_ICON = "mdi-flag-outline";

const route = useRoute();
const router = useRouter();
const store = useTasksStore();

const taskId = String(route.params.id);
const boardId = computed(() => String(route.params.boardId ?? "default"));

onMounted(() => {
    store.get(boardId.value, taskId);
});

/** @type {import('vue').ComputedRef<TaskRead | null>} */
const task = computed(() => store.currentTask);

const editMode = ref(/** @type {EditMode} */ ("none"));
const hasPendingChanges = ref(false);
const isSaving = ref(false);

const isEditingTitle = computed(() => editMode.value === "title");
const isEditingDescription = computed(() => editMode.value === "description");
const isEditingDetails = computed(() => editMode.value === "details");

/**
 * @param {TaskRead | null | undefined} source
 * @returns {TaskDraft}
 */
function getTaskDraft(source) {
    return {
        title: source?.title ?? "",
        description: source?.description ?? "",
        status: source?.status ?? "",
        priority: source?.priority ?? "",
        start_date: source?.start_date ?? "",
        due_date: source?.due_date ?? "",
        estimated_duration_minutes: source?.estimated_duration_minutes ?? null,
    };
}

/**
 * @param {TaskDraft} target
 * @param {TaskDraft} source
 */
function copyDraftValues(target, source) {
    Object.assign(target, source);
}

/**
 * Local editable copy. We intentionally don't mutate `task` directly so
 * Cancel can restore everything without needing to refetch the task.
 */
const draft = reactive(getTaskDraft(null));
const originalDraft = reactive(getTaskDraft(null));

function syncDraftFromTask() {
    if (!task.value) return;

    const values = getTaskDraft(task.value);
    copyDraftValues(draft, values);
    copyDraftValues(originalDraft, values);

    hasPendingChanges.value = false;
}

function beginEdit(/** @type {EditMode} */ mode) {
    if (!task.value) return;

    // If starting a new edit session, make sure the draft reflects
    // the currently displayed task.
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
        const payload = {
            title: draft.title,
            description: draft.description,
            status: draft.status,
            priority: draft.priority,
            start_date: draft.start_date || null,
            due_date: draft.due_date || null,
            estimated_duration_minutes:
                draft.estimated_duration_minutes === ""
                    ? null
                    : draft.estimated_duration_minutes,
        };

        // Adjust this call if your store uses a different update signature.
        await store.update(boardId.value, taskId, payload);

        // If `store.update()` updates currentTask, this keeps the draft
        // aligned with it. Otherwise the local state is still synchronized
        // with what we just submitted.
        copyDraftValues(originalDraft, draft);

        hasPendingChanges.value = false;
        editMode.value = "none";
    } finally {
        isSaving.value = false;
    }
}

watch(
    task,
    (newTask) => {
        if (!newTask) return;

        // Don't overwrite local edits while the user is editing.
        if (editMode.value === "none") {
            syncDraftFromTask();
        }
    },
    { immediate: true }
);

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

const statusOptions = computed(() =>
    Object.entries(STATUS_META).map(([value, meta]) => ({
        value,
        label: meta.label,
        color: meta.color,
        icon: meta.icon,
    }))
);

const priorityOptions = computed(() =>
    Object.keys(PRIORITY_COLORS).map((value) => ({
        value,
        label: value.toUpperCase(),
        color: PRIORITY_COLORS[value] ?? "default",
        icon: PRIORITY_ICONS[value] ?? FALLBACK_PRIORITY_ICON,
    }))
);

const selectedStatus = ref(
    /** @type {TaskStatus | ""} */ (task.value?.status ?? "")
);
const selectedPriority = ref(
    /** @type {TaskPriority | ""} */ (task.value?.priority ?? "")
);

const isSavingStatus = ref(false);
const isSavingPriority = ref(false);

watch(
    task,
    (newTask) => {
        if (!newTask) return;
        selectedStatus.value = newTask.status;
        selectedPriority.value = newTask.priority;
    },
    { immediate: true }
);

/**
 * Shared optimistic-update handler for single-field chip edits (status,
 * priority, ...). Persists the field immediately; on failure, reverts the
 * local ref so the chip snaps back to its previous value.
 *
 * @template {"status" | "priority"} F
 * @param {F} field
 * @param {{ value: string }} item Selected EditableVChip option.
 * @param {import('vue').Ref<string>} localRef Ref bound to the chip's v-model.
 * @param {import('vue').Ref<boolean>} savingRef Ref tracking in-flight save state.
 */
async function updateTaskField(field, item, localRef, savingRef) {
    if (!task.value) return;

    const previousValue = task.value[field];
    savingRef.value = true;

    try {
        await store.update(boardId.value, taskId, { [field]: item.value });
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

const typeIcon = computed(() => {
    const type = task.value?.type;
    return type ? TYPE_ICONS[type] : FALLBACK_TYPE_ICON;
});

const typeLabel = computed(() => {
    const type = task.value?.type;
    return type ? TYPE_LABELS[type] : "Unknown";
});

const isOverdue = computed(() =>
    task.value ? isTaskOverdue(task.value) : false
);

const tags = computed(() => (task.value ? parseTags(task.value.tags) : []));
</script>

<template>
    <div v-if="task" class="task-page">
        <div class="task-page__topbar">
            <v-btn
                icon="mdi-arrow-left"
                variant="text"
                density="comfortable"
                @click="router.back()"
            />

            <div v-if="task.project" class="task-page__crumb">
                <v-icon icon="mdi-folder-outline" size="14" />
                <span>{{ task.project.name }}</span>
            </div>

            <v-spacer />

            <template v-if="editMode !== 'none'">
                <v-btn
                    variant="text"
                    :disabled="isSaving"
                    @click="cancelChanges"
                >
                    Cancel
                </v-btn>

                <v-btn
                    color="primary"
                    variant="tonal"
                    prepend-icon="mdi-content-save-outline"
                    :disabled="!hasPendingChanges"
                    :loading="isSaving"
                    @click="saveChanges"
                >
                    Save
                </v-btn>
            </template>
        </div>

        <header class="task-page__header">
            <div class="task-page__eyebrow">
                <v-icon :icon="typeIcon" size="14" />
                <span>{{ typeLabel }}</span>
            </div>

            <div
                class="editable-field editable-field--title"
                :class="{ 'editable-field--editing': isEditingTitle }"
            >
                <v-text-field
                    v-if="isEditingTitle"
                    v-model="draft.title"
                    label="Title"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    autofocus
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
                    variant="flat"
                    @change="onPriorityChange"
                />

                <span v-if="isOverdue" class="task-page__overdue-flag">
                    <v-icon icon="mdi-calendar-alert" size="14" />
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
                        <v-textarea
                            v-model="draft.description"
                            label="Description"
                            variant="outlined"
                            rows="8"
                            auto-grow
                            hide-details
                        />
                    </div>

                    <div v-else-if="task.description" class="prose">
                        {{ htmlToText(task.description) }}
                    </div>

                    <p v-else class="panel__empty">No description yet.</p>
                </section>

                <section class="panel panel--placeholder">
                    <h2 class="panel__label">Timeline</h2>

                    <div class="gantt-placeholder">
                        <v-icon icon="mdi-chart-gantt" size="26" />
                        <p>Related-task timeline is coming soon.</p>
                    </div>
                </section>
            </main>

            <aside class="task-page__sidebar">
                <div
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

                        <div class="detail-list__row">
                            <dt>Estimate</dt>
                            <dd>
                                {{
                                    formatDuration(
                                        task.estimated_duration_minutes
                                    ) ?? "—"
                                }}
                            </dd>
                        </div>
                    </dl>

                    <div v-else class="detail-editor">
                        <v-text-field
                            :model-value="task.project?.name ?? ''"
                            label="Project"
                            variant="outlined"
                            density="compact"
                            hide-details
                            disabled
                        />

                        <v-text-field
                            v-model="draft.start_date"
                            label="Start"
                            type="date"
                            variant="outlined"
                            density="compact"
                            hide-details
                        />

                        <v-text-field
                            v-model="draft.due_date"
                            label="Due"
                            type="date"
                            variant="outlined"
                            density="compact"
                            hide-details
                        />

                        <v-text-field
                            v-model.number="draft.estimated_duration_minutes"
                            label="Estimate (minutes)"
                            type="number"
                            min="0"
                            variant="outlined"
                            density="compact"
                            hide-details
                        />
                    </div>
                </div>

                <div v-if="tags.length" class="panel">
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
                </div>
            </aside>
        </div>
    </div>
</template>

<style scoped>
.task-page {
    max-width: 960px;
    margin: 0 auto;
    padding: 24px 20px 64px;
}

.task-page__topbar {
    display: flex;
    align-items: center;
    gap: 12px;
}

.task-page__crumb {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8125rem;
    color: rgba(var(--v-theme-on-surface), 0.65);
}

.task-page__header {
    padding: 20px 0 28px;
    margin-bottom: 28px;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.task-page__eyebrow {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.task-page__title {
    margin: 0;
    font-size: 1.75rem;
    font-weight: 600;
    line-height: 1.25;
}

.task-page__badges {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.task-page__status-select {
    width: 160px;
}

.task-page__priority-select {
    width: 160px;
}

.task-page__overdue-flag {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8125rem;
    font-weight: 600;
    color: rgb(var(--v-theme-error));
}

.task-page__body {
    display: grid;
    grid-template-columns: 1fr 280px;
    align-items: start;
    gap: 28px;
}

@media (max-width: 760px) {
    .task-page__body {
        grid-template-columns: 1fr;
    }
}

.task-page__main {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0;
}

.task-page__sidebar {
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: sticky;
    top: 20px;
}

@media (max-width: 760px) {
    .task-page__sidebar {
        position: static;
    }
}

.panel {
    padding: 20px 22px;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-radius: 12px;
    background: rgb(var(--v-theme-surface));
}

.panel--placeholder {
    background: transparent;
    border-style: dashed;
}

.panel--editing {
    border-color: rgba(var(--v-theme-primary), 0.35);
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 14px;
}

.panel__heading .panel__label {
    margin-bottom: 0;
}

.panel__label {
    margin: 0 0 14px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.panel__edit-btn {
    opacity: 0;
    transition: opacity 0.15s ease;
}

.panel:hover .panel__edit-btn,
.panel__edit-btn:focus-visible {
    opacity: 1;
}

.panel__empty {
    margin: 0;
    font-size: 0.875rem;
    font-style: italic;
    color: rgba(var(--v-theme-on-surface), 0.5);
}

.editable-field {
    position: relative;
}

.editable-field__display {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.editable-field__edit-btn {
    opacity: 0;
    transition: opacity 0.15s ease;
}

.editable-field:hover .editable-field__edit-btn,
.editable-field__edit-btn:focus-visible {
    opacity: 1;
}

.editable-field--editing {
    max-width: 700px;
}

.prose {
    max-width: 68ch;
    font-size: 0.9375rem;
    line-height: 1.7;
    color: rgba(var(--v-theme-on-surface), 0.87);
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
}

.gantt-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 28px 16px;
    color: rgba(var(--v-theme-on-surface), 0.4);
    text-align: center;
}

.gantt-placeholder p {
    margin: 0;
    font-size: 0.8125rem;
}

.detail-list {
    margin: 0;
}

.detail-list__row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 7px 0;
    font-size: 0.8125rem;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.detail-list__row:last-child {
    border-bottom: none;
}

.detail-list__row dt {
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.detail-list__row dd {
    margin: 0;
    font-weight: 500;
    text-align: right;
}

.detail-list__row dd.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.detail-editor {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
</style>
