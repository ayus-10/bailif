<script setup>
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";
import { htmlPreview } from "@/utils/htmlFormatters";
import { formatDate, isTaskOverdue, parseTags } from "@/utils/taskFormatters";

/** @typedef {import('@/types/task').TaskRead} TaskRead */

const props = defineProps({
    task: {
        /** @type {import('vue').PropType<TaskRead>} */
        type: Object,
        required: true,
    },
    sortable: {
        type: Boolean,
        default: false,
    },
});

const router = useRouter();

const isOverdue = computed(() => isTaskOverdue(props.task));
const tagCount = computed(() => parseTags(props.task.tags).length);

const emit = defineEmits(["complete", "snooze", "delete", "duplicate"]);

const isExpanded = ref(false);
const isHovering = ref(false);
const contextMenuOpen = ref(false);

/** @type {import("vue").Ref<[number, number]>} */
const contextMenuTarget = ref([0, 0]);

function toggleDescription() {
    isExpanded.value = !isExpanded.value;
}

/** @param {MouseEvent} e */
function openContextMenu(e) {
    contextMenuTarget.value = [e.clientX, e.clientY];
    contextMenuOpen.value = true;
}

function goToTask() {
    router.push(`/tasks/${props.task.id}`);
}

/** @param {MouseEvent} e */
function handleComplete(e) {
    e.stopPropagation();
    emit("complete", props.task);
}

/** @param {MouseEvent} e */
function handleSnooze(e) {
    e.stopPropagation();
    emit("snooze", props.task);
}

/** @param {MouseEvent} e */
function handleDelete(e) {
    e.stopPropagation();
    emit("delete", props.task);
}

/** @param {MouseEvent} e */
function handleDuplicate(e) {
    e.stopPropagation();
    emit("duplicate", props.task);
}
</script>

<template>
    <v-card
        variant="outlined"
        rounded="lg"
        class="task-row"
        :class="{
            'task-row--overdue': isOverdue,
            'task-row--complete': task.status === 'done',
        }"
        tabindex="0"
        role="button"
        :aria-label="`Open task: ${task.title}`"
        @click="goToTask"
        @keydown.enter="goToTask"
        @mouseenter="isHovering = true"
        @mouseleave="isHovering = false"
        @contextmenu.prevent="openContextMenu"
    >
        <div class="task-row__controls">
            <button
                class="task-row__drag"
                type="button"
                tabindex="-1"
                aria-label="Drag to reorder"
                @click.stop
                @mousedown.stop
            >
                <v-icon icon="mdi-drag-vertical" size="16" />
            </button>

            <button
                class="task-row__toggle"
                type="button"
                :aria-label="
                    isExpanded ? 'Collapse description' : 'Expand description'
                "
                @click.stop="toggleDescription"
            >
                <v-icon
                    :icon="
                        isExpanded ? 'mdi-chevron-down' : 'mdi-chevron-right'
                    "
                    size="16"
                />
            </button>
        </div>

        <div class="task-row__body">
            <div class="task-row__title-row">
                <span class="task-row__title text-body-2 font-weight-medium">
                    {{ task.title }}
                </span>
            </div>

            <div class="task-row__meta-row">
                <div class="task-row__meta-left">
                    <div v-if="tagCount" class="task-row__meta">
                        <v-icon icon="mdi-tag-outline" size="12" />
                        <span>{{ tagCount }}</span>
                    </div>

                    <div
                        v-if="task.due_date"
                        class="task-row__meta"
                        :class="{ overdue: isOverdue }"
                    >
                        <v-icon
                            :icon="
                                isOverdue
                                    ? 'mdi-calendar-alert'
                                    : 'mdi-calendar-blank-outline'
                            "
                            size="12"
                        />
                        <span>{{ formatDate(task.due_date) }}</span>
                    </div>

                    <div
                        v-if="task.estimated_duration_minutes"
                        class="task-row__meta"
                    >
                        <v-icon icon="mdi-timer-outline" size="12" />
                        <span>{{ task.estimated_duration_minutes }}m</span>
                    </div>

                    <v-chip
                        size="x-small"
                        variant="tonal"
                        class="task-row__priority"
                        :color="PRIORITY_COLORS[task.priority] ?? 'default'"
                    >
                        {{ task.priority.toUpperCase() }}
                    </v-chip>
                </div>
            </div>

            <p
                v-if="isExpanded && task.description"
                class="task-row__description text-caption"
            >
                {{ htmlPreview(task.description) }}
            </p>
        </div>

        <div
            class="task-row__actions"
            :class="{ 'task-row__actions--visible': isHovering }"
        >
            <v-tooltip text="Snooze" location="left" v-if="isExpanded">
                <template #activator="{ props: tip }">
                    <button
                        v-bind="tip"
                        type="button"
                        class="task-row__action-btn"
                        @click="handleSnooze"
                    >
                        <v-icon icon="mdi-clock-outline" size="16" />
                    </button>
                </template>
            </v-tooltip>

            <v-tooltip text="Delete" location="left" v-if="isExpanded">
                <template #activator="{ props: tip }">
                    <button
                        v-bind="tip"
                        type="button"
                        class="task-row__action-btn task-row__action-btn--danger"
                        @click="handleDelete"
                    >
                        <v-icon icon="mdi-trash-can-outline" size="16" />
                    </button>
                </template>
            </v-tooltip>

            <v-menu location="bottom end">
                <template #activator="{ props: menuProps }">
                    <button
                        v-bind="menuProps"
                        type="button"
                        class="task-row__action-btn"
                        @click.stop
                    >
                        <v-icon icon="mdi-dots-horizontal" size="16" />
                    </button>
                </template>
                <v-list density="compact">
                    <v-list-item
                        prepend-icon="mdi-check"
                        :title="
                            task.status === 'done'
                                ? 'Mark incomplete'
                                : 'Mark complete'
                        "
                        @click="handleComplete"
                    />
                    <v-list-item
                        prepend-icon="mdi-clock-outline"
                        title="Snooze"
                        @click="handleSnooze"
                    />
                    <v-list-item
                        prepend-icon="mdi-content-copy"
                        title="Duplicate"
                        @click="handleDuplicate"
                    />
                    <v-divider />
                    <v-list-item
                        prepend-icon="mdi-trash-can-outline"
                        title="Delete"
                        class="text-error"
                        @click="handleDelete"
                    />
                </v-list>
            </v-menu>
        </div>

        <v-menu v-model="contextMenuOpen" :target="contextMenuTarget">
            <v-list density="compact">
                <v-list-item
                    prepend-icon="mdi-check"
                    :title="
                        task.status === 'done'
                            ? 'Mark incomplete'
                            : 'Mark complete'
                    "
                    @click="handleComplete"
                />
                <v-list-item
                    prepend-icon="mdi-clock-outline"
                    title="Snooze"
                    @click="handleSnooze"
                />
                <v-list-item
                    prepend-icon="mdi-content-copy"
                    title="Duplicate"
                    @click="handleDuplicate"
                />
                <v-divider />
                <v-list-item
                    prepend-icon="mdi-trash-can-outline"
                    title="Delete"
                    class="text-error"
                    @click="handleDelete"
                />
            </v-list>
        </v-menu>
    </v-card>
</template>

<style scoped>
.task-row {
    position: relative;
    display: grid;
    grid-template-columns: 20px minmax(0, 1fr) auto;
    grid-auto-rows: auto;
    align-items: stretch;
    align-self: start;
    column-gap: 8px;
    width: 100%;
    min-width: 0;
    height: fit-content;
    padding: 8px 12px;
    overflow: hidden;
    cursor: pointer;
    user-select: none;
    background-color: rgba(var(--v-theme-on-surface), 0.015);
    border-color: rgba(var(--v-theme-on-surface), 0.08);
    transition:
        background-color 0.12s ease,
        border-color 0.12s ease,
        box-shadow 0.12s ease;
}

.task-row__controls {
    grid-column: 1;
    grid-row: 1 / -1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 20px;
    min-width: 20px;
    height: fit-content;
    align-self: center;
    gap: 2px;
}

.task-row:hover {
    background-color: rgba(var(--v-theme-on-surface), 0.035);
    border-color: rgba(var(--v-theme-on-surface), 0.14);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.task-row:focus {
    outline: none;
}

.task-row:focus-visible {
    outline: 2px solid rgb(var(--v-theme-primary));
    outline-offset: -1px;
}

.task-row--complete {
    background-color: rgba(var(--v-theme-on-surface), 0.01);
    border-color: rgba(var(--v-theme-on-surface), 0.07);
}

.task-row--complete .task-row__title {
    color: rgba(var(--v-theme-on-surface), 0.5);
    text-decoration: line-through;
}

.task-row--overdue {
    background-color: rgba(var(--v-theme-on-surface), 0.015);
    border-color: rgba(var(--v-theme-on-surface), 0.08);
}

.task-row--overdue:hover {
    background-color: rgba(var(--v-theme-on-surface), 0.035);
    border-color: rgba(var(--v-theme-on-surface), 0.14);
}

.task-row__drag,
.task-row__toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    min-width: 20px;
    height: 20px;
    padding: 0;
    border: none;
    background: none;
    cursor: pointer;
}

.task-row__drag {
    color: rgba(var(--v-theme-on-surface), 0.35);
    cursor: grab;
    opacity: 0;
    transition: opacity 0.12s ease;
}

.task-row__toggle {
    color: rgba(var(--v-theme-on-surface), 0.4);
    opacity: 0;
    transition:
        opacity 0.12s ease,
        color 0.12s ease;
}

.task-row__toggle:hover {
    color: rgba(var(--v-theme-on-surface), 0.8);
}

.task-row:hover .task-row__drag,
.task-row:focus-within .task-row__drag,
.task-row:hover .task-row__toggle,
.task-row:focus-within .task-row__toggle {
    opacity: 1;
}

.task-row__body {
    grid-column: 2;
    grid-row: 1 / -1;
    min-width: 0;
    width: 100%;
    height: fit-content;
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 2px 0;
}

.task-row__title-row {
    display: flex;
    align-items: center;
    min-height: 20px;
}

.task-row__title {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-row__meta-row {
    display: flex;
    align-items: center;
    min-width: 0;
    width: 100%;
    gap: 8px;
}

.task-row__meta-left {
    display: flex;
    align-items: center;
    min-width: 0;
    gap: 12px;
    flex-wrap: wrap;
}

.task-row__meta {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 0.6875rem;
    font-variant-numeric: tabular-nums;
    color: rgba(var(--v-theme-on-surface), 0.6);
    white-space: nowrap;
}

.task-row__meta.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.task-row__priority {
    flex: 0 0 auto;
    flex-shrink: 0;
    font-weight: 600;
}

.task-row__description {
    margin: 0;
    min-width: 0;
    max-width: 100%;
    color: rgba(var(--v-theme-on-surface), 0.6);
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
}

.task-row__actions {
    grid-column: 3;
    grid-row: 1 / -1;
    align-self: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    min-width: 28px;
    height: fit-content;
    padding: 2px 0;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.12s ease;
}

.task-row__actions--visible,
.task-row:focus-within .task-row__actions {
    opacity: 1;
    pointer-events: auto;
}

.task-row__action-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    padding: 0;
    border: none;
    border-radius: 6px;
    background: none;
    color: rgba(var(--v-theme-on-surface), 0.6);
    cursor: pointer;
    transition:
        background-color 0.12s ease,
        color 0.12s ease;
}

.task-row__action-btn:hover {
    background-color: rgba(var(--v-theme-on-surface), 0.06);
    color: rgba(var(--v-theme-on-surface), 0.9);
}

.task-row__action-btn--danger:hover {
    background-color: rgba(var(--v-theme-error), 0.1);
    color: rgb(var(--v-theme-error));
}

.task-row__action-btn:focus-visible {
    outline: 2px solid rgb(var(--v-theme-primary));
    outline-offset: 1px;
}

@media (max-width: 640px) {
    .task-row {
        grid-template-columns: 20px minmax(0, 1fr) auto;
        column-gap: 6px;
        padding: 8px;
        height: fit-content;
        align-self: start;
    }

    .task-row__body {
        height: fit-content;
    }

    .task-row__meta-left {
        gap: 8px;
    }

    .task-row__meta-left .task-row__meta:not(:first-child):not(:last-child) {
        display: none;
    }

    .task-row__actions {
        height: fit-content;
    }
}
</style>
