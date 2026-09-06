<script setup>
import { useRoute, useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import TaskColumn from "@/components/tasks/TaskColumn.vue";
import { TASK_COLUMNS } from "@/constants/tasks";
import { useTaskboardsStore } from "@/stores/taskboard.store";
import { useTasksStore } from "@/stores/tasks.store";

/** @typedef {import('@/types/task').TaskRead} TaskRead */
/** @typedef {import('@/types/task').TaskCreate} TaskCreate */
/** @typedef {import('@/types/task').TaskQueryMode} TaskQueryMode */

const BOARD_CONFIG = Object.freeze({
    board: {
        name: "Your taskboard",
        description: "Plan, prioritize, and track work across the project.",
    },
    icon: {
        fallback: "mdi-view-dashboard-outline",
        size: "1.125rem",
    },
    visibility: {
        fallback: "Private",
    },
    actions: {
        iconSize: "1.125rem",
        share: {
            key: "share",
            label: "Share board",
            icon: "mdi-share-variant-outline",
        },
        settings: {
            key: "settings",
            label: "Board settings",
            icon: "mdi-cog-outline",
        },
        invite: {
            key: "invite",
            label: "Invite people",
        },
    },
    invite: {
        label: "Invite people",
        icon: "mdi-account-plus-outline",
        color: "primary",
        density: "compact",
    },
    search: {
        placeholder: "Search tasks",
        icon: "mdi-magnify",
        variant: "outlined",
        density: "compact",
        hideDetails: true,
    },
    toolbar: {
        iconSize: "1rem",
        chevronSize: "0.875rem",
        chevron: "mdi-chevron-down",
        filter: {
            key: "filter",
            label: "Filter",
            icon: "mdi-filter-variant",
        },
        sort: {
            key: "sort",
            label: "Sort",
            icon: "mdi-sort-variant",
        },
        view: {
            key: "view",
            label: "View",
            icon: "mdi-view-grid-outline",
        },
    },
    createButton: {
        label: "New task",
        icon: "mdi-plus",
        color: "primary",
        density: "compact",
    },
});

const route = useRoute();
const router = useRouter();

const projectId = ref(localStorage.getItem("project_id") ?? ""); // TODO: replace with session

const currentBoard = computed(() => {
    const id = route.params.id;

    if (!id || id === "all") {
        return { type: "all" };
    }

    return {
        type: "board",
        id: Array.isArray(id) ? id[0] : id,
    };
});

/** @type {import('vue').Ref<TaskQueryMode>} */
const preferredQueryMode = ref("root-tasks"); // TODO: it was supposed to allow all, but wtf is going on?

const query = computed(() => ({
    queryMode: preferredQueryMode.value,
    taskboardId:
        currentBoard.value.type === "board" ? currentBoard.value.id : null,
    // TODO: add more TaskFetchOptions
}));

const taskboardsStore = useTaskboardsStore();
const tasksStore = useTasksStore();

onMounted(() => {
    if (currentBoard.value.type === "board" && currentBoard.value.id)
        taskboardsStore.get(currentBoard.value.id);
    tasksStore.fetch(projectId.value, query.value);
});

const tasks = computed(() =>
    tasksStore.tasksByQuery(projectId.value, query.value)
);

const status = computed(() =>
    tasksStore.statusByQuery(projectId.value, query.value)
);

const error = computed(() =>
    tasksStore.errorByQuery(projectId.value, query.value)
);

const filteredTasks = computed(() => {
    return tasks.value.filter((task) => {
        if (route.query.status && task.status !== route.query.status)
            return false;

        if (route.query.priority && task.priority !== route.query.priority)
            return false;

        return true;
    });
});

const tasksByStatus = computed(() => {
    return filteredTasks.value.reduce((acc, task) => {
        if (!acc[task.status]) acc[task.status] = [];

        acc[task.status].push(task);
        return acc;
    }, /** @type {Record<string, TaskRead[]>} */ ({}));
});

const searchQuery = ref("");
const activeFilterCount = ref(0);

const hasActiveFilters = computed(() => activeFilterCount.value > 0);

function handleAction(action) {
    console.log(action);
}

const draggedTask = ref(/** @type {TaskRead | null} */ (null));

/** @type {import('vue').Ref<TaskCreate | null>} */
const pendingTask = ref(null);

function retry() {
    if (currentBoard.value.type === "board" && currentBoard.value.id)
        taskboardsStore.get(currentBoard.value.id, { forceRefresh: true });
    tasksStore.fetch(projectId.value, { ...query.value, forceRefresh: true });
}

/** @param {string} key */
function clearFilter(key) {
    const query = { ...route.query };

    delete query[key];

    router.push({
        path: route.path,
        query,
    });
}

/** @param {TaskRead} task */
function startDrag(task) {
    draggedTask.value = task;
}

/** @param {TaskRead["status"]} targetStatus */
async function dropTask(targetStatus) {
    if (!draggedTask.value) return;

    const task = draggedTask.value;

    if (task.status === targetStatus) {
        draggedTask.value = null;
        return;
    }

    const oldStatus = task.status;
    task.status = targetStatus;

    try {
        await tasksStore.update(task.id, {
            status: targetStatus,
        });
    } catch (err) {
        task.status = oldStatus;
        console.error(err);
    } finally {
        draggedTask.value = null;
    }
}

function openNewTask() {
    pendingTask.value = {
        project_id: projectId.value,
        title: "",
        status: "open",
    };
}

function handleClear() {
    pendingTask.value = null;
}
</script>

<template>
    <v-container fluid class="task-board">
        <header class="task-board__header">
            <div class="task-board__identity">
                <div class="task-board__icon">
                    <v-icon :size="BOARD_CONFIG.icon.size">
                        {{ BOARD_CONFIG.icon.fallback }}
                    </v-icon>
                </div>

                <div class="task-board__identity-content">
                    <div class="task-board__title-row">
                        <h1 class="task-board__title">
                            {{ BOARD_CONFIG.board.name }}
                        </h1>

                        <span class="task-board__visibility">
                            {{ BOARD_CONFIG.visibility.fallback }}
                        </span>
                    </div>

                    <p class="task-board__description">
                        {{ BOARD_CONFIG.board.description }}
                    </p>
                </div>
            </div>

            <div class="task-board__actions">
                <button
                    type="button"
                    class="task-board__icon-button"
                    :aria-label="BOARD_CONFIG.actions.share.label"
                    @click="handleAction(BOARD_CONFIG.actions.share.key)"
                >
                    <v-icon :size="BOARD_CONFIG.actions.iconSize">
                        {{ BOARD_CONFIG.actions.share.icon }}
                    </v-icon>
                </button>

                <button
                    type="button"
                    class="task-board__icon-button"
                    :aria-label="BOARD_CONFIG.actions.settings.label"
                    @click="handleAction(BOARD_CONFIG.actions.settings.key)"
                >
                    <v-icon :size="BOARD_CONFIG.actions.iconSize">
                        {{ BOARD_CONFIG.actions.settings.icon }}
                    </v-icon>
                </button>

                <v-btn
                    :color="BOARD_CONFIG.invite.color"
                    :prepend-icon="BOARD_CONFIG.invite.icon"
                    variant="flat"
                    :density="BOARD_CONFIG.invite.density"
                    class="text-none task-board__invite"
                    @click="handleAction(BOARD_CONFIG.actions.invite.key)"
                >
                    {{ BOARD_CONFIG.invite.label }}
                </v-btn>
            </div>
        </header>

        <div class="task-board__toolbar">
            <div class="task-board__toolbar-left">
                <v-text-field
                    v-model="searchQuery"
                    :placeholder="BOARD_CONFIG.search.placeholder"
                    :prepend-inner-icon="BOARD_CONFIG.search.icon"
                    :density="BOARD_CONFIG.search.density"
                    :hide-details="BOARD_CONFIG.search.hideDetails"
                    :variant="BOARD_CONFIG.search.variant"
                    class="task-board__search"
                />

                <button
                    type="button"
                    class="task-board__toolbar-button"
                    :class="{
                        'task-board__toolbar-button--active': hasActiveFilters,
                    }"
                    @click="handleAction(BOARD_CONFIG.toolbar.filter.key)"
                >
                    <v-icon :size="BOARD_CONFIG.toolbar.iconSize">
                        {{ BOARD_CONFIG.toolbar.filter.icon }}
                    </v-icon>

                    <span>{{ BOARD_CONFIG.toolbar.filter.label }}</span>

                    <span
                        v-if="activeFilterCount > 0"
                        class="task-board__toolbar-count"
                    >
                        {{ activeFilterCount }}
                    </span>
                </button>

                <button
                    type="button"
                    class="task-board__toolbar-button"
                    @click="handleAction(BOARD_CONFIG.toolbar.sort.key)"
                >
                    <v-icon :size="BOARD_CONFIG.toolbar.iconSize">
                        {{ BOARD_CONFIG.toolbar.sort.icon }}
                    </v-icon>

                    <span>{{ BOARD_CONFIG.toolbar.sort.label }}</span>
                </button>

                <button
                    type="button"
                    class="task-board__toolbar-button"
                    @click="handleAction(BOARD_CONFIG.toolbar.view.key)"
                >
                    <v-icon :size="BOARD_CONFIG.toolbar.iconSize">
                        {{ BOARD_CONFIG.toolbar.view.icon }}
                    </v-icon>

                    <span>{{ BOARD_CONFIG.toolbar.view.label }}</span>

                    <v-icon :size="BOARD_CONFIG.toolbar.chevronSize">
                        {{ BOARD_CONFIG.toolbar.chevron }}
                    </v-icon>
                </button>
            </div>

            <v-btn
                :color="BOARD_CONFIG.createButton.color"
                :prepend-icon="BOARD_CONFIG.createButton.icon"
                variant="flat"
                :density="BOARD_CONFIG.createButton.density"
                class="text-none task-board__new-task"
                @click="openNewTask"
            >
                {{ BOARD_CONFIG.createButton.label }}
            </v-btn>
        </div>

        <div class="task-board__content">
            <div class="task-board__columns">
                <TaskColumn
                    v-for="column in TASK_COLUMNS"
                    :key="column.status"
                    :column="column"
                    :tasks="tasksByStatus[column.status] ?? []"
                    :pending-task="pendingTask"
                    :project-id="projectId"
                    :taskboard-id="
                        currentBoard.type === 'board' ? currentBoard.id : null
                    "
                    @drag-start="startDrag"
                    @drop="dropTask"
                    @clear-pending-task="handleClear"
                />
            </div>
        </div>
    </v-container>
</template>

<style scoped>
.task-board {
    height: 100%;
    min-width: 0;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    background: var(--v-theme-surface, #ffffff);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.task-board__header {
    flex: 0 0 auto;
    min-height: 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
}

.task-board__identity {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.625rem;
}

.task-board__icon {
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0.0625rem solid var(--v-theme-outline, #e1e4e8);
    border-radius: 0.375rem;
    background: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface-variant, #475467);
}

.task-board__identity-content {
    min-width: 0;
}

.task-board__title-row {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.task-board__title {
    margin: 0;
    overflow: hidden;
    color: var(--v-theme-on-surface, #1a1f2c);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-board__visibility {
    flex: 0 0 auto;
    padding: 0.125rem 0.375rem;
    border: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
    border-radius: 0.125rem;
    color: var(--v-theme-on-surface-variant, #475467);
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.task-board__description {
    margin: 0.125rem 0 0;
    overflow: hidden;
    color: var(--v-theme-on-surface-variant, #475467);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-board__actions {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.task-board__icon-button {
    width: 2rem;
    height: 2rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: 0.0625rem solid transparent;
    border-radius: 0.375rem;
    background: transparent;
    color: var(--v-theme-on-surface-variant, #475467);
    cursor: pointer;
}

.task-board__icon-button:hover {
    border-color: var(--v-theme-outline, #e1e4e8);
    background: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.task-board__invite {
    margin-left: 0.25rem;
}

.task-board__toolbar {
    flex: 0 0 auto;
    min-height: 3.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
}

.task-board__toolbar-left {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.task-board__search {
    width: 16rem;
    margin-right: 0.375rem;
}

.task-board__toolbar-button {
    min-height: 2rem;
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0 0.625rem;
    border: 0.0625rem solid transparent;
    border-radius: 0.375rem;
    background: transparent;
    color: var(--v-theme-on-surface-variant, #475467);
    font-size: 0.8125rem;
    font-weight: 600;
    line-height: 1rem;
    cursor: pointer;
}

.task-board__toolbar-button:hover {
    border-color: var(--v-theme-outline, #e1e4e8);
    background: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.task-board__toolbar-button--active {
    border-color: var(--v-theme-accent, #7c3aed);
    color: var(--v-theme-accent, #7c3aed);
}

.task-board__toolbar-count {
    min-width: 1rem;
    height: 1rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 0.25rem;
    border-radius: 0.125rem;
    background: var(--v-theme-accent, #7c3aed);
    color: var(--v-theme-on-primary, #ffffff);
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
}

.task-board__new-task {
    flex: 0 0 auto;
}

.task-board__content {
    flex: 1 1 auto;
    min-height: 0;
    min-width: 0;
    padding-top: 0.75rem;
    overflow-x: auto;
    overflow-y: hidden;
}

.task-board__columns {
    height: 100%;
    min-width: max-content;
    display: flex;
    flex-wrap: nowrap;
    align-items: stretch;
    gap: 0.75rem;
}

.task-board__columns > :deep(.task-column) {
    flex: 0 0 33%;
}

:deep(.task-board__search .v-field) {
    --v-field-border-opacity: 1;
}

:deep(.task-board__search .v-field__outline) {
    color: var(--v-theme-outline, #e1e4e8);
}

:deep(.task-board__search .v-field--focused .v-field__outline) {
    color: var(--v-theme-primary, #1976d2);
}
</style>
