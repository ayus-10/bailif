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
    accentColor: {
        type: String,
        default: null,
    },
});

const router = useRouter();

const isOverdue = computed(() => isTaskOverdue(props.task));
const tagCount = computed(() => parseTags(props.task.tags).length);

// TODO: TaskRead doesn't define `progress` yet
const progressValue = 67;

const emit = defineEmits([
    "complete",
    "snooze",
    "delete",
    "duplicate",
    "dragstart",
    "dragend",
]);

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
        draggable="true"
        variant="outlined"
        rounded="lg"
        class="task-card"
        :style="{ '--task-accent': accentColor }"
        :class="{
            'task-card--overdue': isOverdue,
            'task-card--complete': task.status === 'done',
        }"
        tabindex="0"
        role="button"
        :aria-label="`Open task: ${task.title}`"
        @click="goToTask"
        @keydown.enter="goToTask"
        @mouseenter="isHovering = true"
        @mouseleave="isHovering = false"
        @contextmenu.prevent="openContextMenu"
        @dragstart="$emit('dragstart', $event)"
        @dragend="$emit('dragend')"
    >
        <div
            class="task-card__toolbar"
            :class="{ 'task-card__toolbar--visible': isHovering }"
        >
            <v-menu location="bottom end">
                <template #activator="{ props: menuProps }">
                    <button
                        v-bind="menuProps"
                        type="button"
                        class="task-card__icon-btn"
                        v-ripple
                        @click.stop
                    >
                        <v-icon icon="mdi-dots-horizontal" size="14" />
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

        <div class="task-card__top">
            <v-chip
                size="x-small"
                variant="tonal"
                class="task-card__priority"
                :color="PRIORITY_COLORS[task.priority] ?? 'default'"
            >
                {{ task.priority.toUpperCase() }}
            </v-chip>

            <span v-if="isOverdue" class="task-card__overdue-flag">
                <v-icon icon="mdi-calendar-alert" size="12" />
                Overdue
            </span>
        </div>

        <h3 class="task-card__title">{{ task.title }}</h3>

        <p v-if="task.description" class="task-card__description">
            {{ htmlPreview(task.description) }}
        </p>

        <div class="task-card__progress-row">
            <span class="task-card__progress-label">Progress</span>
            <span class="task-card__progress-value">{{ progressValue }}%</span>
        </div>

        <div class="task-card__progress-track">
            <div
                class="task-card__progress-fill"
                :style="{ width: progressValue + '%' }"
            />
        </div>

        <div class="task-card__footer">
            <div v-if="tagCount" class="task-card__meta">
                <v-icon icon="mdi-tag-outline" size="12" />
                <span>{{ tagCount }}</span>
            </div>

            <div
                v-if="task.due_date"
                class="task-card__meta"
                :class="{ 'task-card__meta--overdue': isOverdue }"
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
.task-card {
    --task-accent: rgb(var(--v-theme-primary));

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem 0.875rem;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    border-radius: 0.75rem;
    background-color: rgb(var(--v-theme-surface));
    border-color: rgb(var(--v-theme-outline-variant, 234, 236, 240));
    transition:
        border-color 0.12s ease,
        background-color 0.12s ease;
}

.task-card:hover {
    border-color: color-mix(
        in srgb,
        var(--task-accent) 22%,
        rgb(var(--v-theme-outline-variant, 234, 236, 240))
    );
    background-color: color-mix(
        in srgb,
        var(--task-accent) 3%,
        rgb(var(--v-theme-surface))
    );
}

.task-card:focus {
    outline: none;
}

.task-card:focus-visible {
    outline: 0.125rem solid
        color-mix(in srgb, var(--task-accent) 55%, transparent);
    outline-offset: 0.125rem;
}

.task-card--complete {
    background-color: color-mix(
        in srgb,
        var(--task-accent) 2%,
        rgb(var(--v-theme-grey-lighten-4, 245, 246, 248))
    );
}

.task-card--complete .task-card__title {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    text-decoration: line-through;
}

.task-card--overdue {
    border-color: rgba(var(--v-theme-error), 0.35);
}

.task-card__toolbar {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    display: flex;
    align-items: center;
    opacity: 0;
    transition: opacity 0.12s ease;
    z-index: 1;
}

.task-card__toolbar--visible,
.task-card:focus-within .task-card__toolbar {
    opacity: 1;
}

.task-card__icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    border: none;
    border-radius: 0.375rem;
    background: rgb(var(--v-theme-surface));
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
}

.task-card__icon-btn:hover {
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
    color: rgb(var(--v-theme-on-surface));
}

.task-card__icon-btn:focus-visible {
    outline: 0.125rem solid
        color-mix(in srgb, var(--task-accent) 55%, transparent);
    outline-offset: 0.0625rem;
}

.task-card__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    padding-right: 2rem;
}

.task-card__priority {
    flex: 0 0 auto;
    padding: 0.125rem 0.375rem;
    border: 0.0625rem solid currentColor;
    border-radius: 0.125rem;
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    user-select: none;
    -webkit-user-select: none;
}

.task-card__overdue-flag {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    color: rgb(var(--v-theme-error));
    font-size: 0.6875rem;
    font-weight: 700;
    white-space: nowrap;
}

.task-card__title {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-card__description {
    margin: 0;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    line-height: 1.35rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
}

.task-card__progress-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.125rem;
}

.task-card__progress-label {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.75rem;
    font-weight: 600;
}

.task-card__progress-value {
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.75rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

.task-card__progress-track {
    position: relative;
    width: 100%;
    height: 0.375rem;
    border-radius: 999px;
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
    overflow: hidden;
}

.task-card__progress-fill {
    height: 100%;
    border-radius: 999px;
    background: var(--task-accent);
    transition: width 0.2s ease;
}

.task-card--complete .task-card__progress-fill {
    background: rgb(var(--v-theme-success, 76, 175, 80));
}
</style>
