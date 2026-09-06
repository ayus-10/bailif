<script setup>
import { computed, ref } from "vue";

const CONFIG = {
    search: {
        icon: "mdi-magnify",
        hideDetails: true,
        label: "Search tasks",
    },
    actions: {
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
    icons: {
        chevron: "mdi-chevron-down",
        size: "1rem",
        chevronSize: "0.875rem",
    },
    createButton: {
        icon: "mdi-plus",
        color: "primary",
        label: "New task",
    },
};

const emit = defineEmits(["action", "new-task"]);

const searchQuery = ref("");
const activeFilterCount = ref(0);

const hasActiveFilters = computed(() => activeFilterCount.value > 0);

/** @param {String} action */
function handleAction(action) {
    emit("action", action);
}

function handleNewTask() {
    emit("new-task");
}
</script>

<template>
    <div class="board-toolbar">
        <div class="board-toolbar__left">
            <v-text-field
                v-model="searchQuery"
                :placeholder="CONFIG.search.label"
                :prepend-inner-icon="CONFIG.search.icon"
                density="compact"
                :hide-details="CONFIG.search.hideDetails"
                variant="outlined"
                class="board-toolbar__search"
            >
                <template #append-inner>
                    <span
                        class="board-toolbar__search-shortcut"
                        aria-label="Command S"
                    >
                        <kbd>⌘</kbd><kbd>S</kbd>
                    </span>
                </template>
            </v-text-field>

            <button
                v-ripple
                type="button"
                class="board-toolbar__button"
                :class="{
                    'board-toolbar__button--active': hasActiveFilters,
                }"
                @click="handleAction(CONFIG.actions.filter.key)"
            >
                <v-icon :size="CONFIG.icons.size">
                    {{ CONFIG.actions.filter.icon }}
                </v-icon>

                <span>{{ CONFIG.actions.filter.label }}</span>

                <span v-if="activeFilterCount > 0" class="board-toolbar__count">
                    {{ activeFilterCount }}
                </span>
            </button>

            <button
                v-ripple
                type="button"
                class="board-toolbar__button"
                @click="handleAction(CONFIG.actions.sort.key)"
            >
                <v-icon :size="CONFIG.icons.size">
                    {{ CONFIG.actions.sort.icon }}
                </v-icon>

                <span>{{ CONFIG.actions.sort.label }}</span>
            </button>

            <button
                v-ripple
                type="button"
                class="board-toolbar__button"
                @click="handleAction(CONFIG.actions.view.key)"
            >
                <v-icon :size="CONFIG.icons.size">
                    {{ CONFIG.actions.view.icon }}
                </v-icon>

                <span>{{ CONFIG.actions.view.label }}</span>

                <v-icon :size="CONFIG.icons.chevronSize">
                    {{ CONFIG.icons.chevron }}
                </v-icon>
            </button>
        </div>

        <v-btn
            :color="CONFIG.createButton.color"
            :prepend-icon="CONFIG.createButton.icon"
            variant="flat"
            density="comfortable"
            class="text-none board-toolbar__new-task"
            @click="handleNewTask"
        >
            {{ CONFIG.createButton.label }}
        </v-btn>
    </div>
</template>

<style scoped>
.board-toolbar {
    flex: 0 0 auto;
    min-height: 3.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 0.0625rem solid
        rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.board-toolbar__left {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex: 1 1 auto;
}

.board-toolbar__button {
    min-height: 2.25rem;
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0 0.75rem;
    border: 0.0625rem solid transparent;
    border-radius: 0.5rem;
    background: transparent;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    font-weight: 500;
    line-height: 1rem;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    position: relative;
    overflow: hidden;
    isolation: isolate;
    transition:
        background-color 0.15s ease,
        color 0.15s ease,
        border-color 0.15s ease;
}

.board-toolbar__button:hover {
    background: rgb(var(--v-theme-on-surface), 0.05);
    background: rgba(25, 118, 210, 0.06);
    color: rgb(var(--v-theme-on-surface, 26, 31, 44));
}

.board-toolbar__button:focus-visible {
    outline: none;
    border-color: rgba(25, 118, 210, 0.5);
    box-shadow: 0 0 0 0.1875rem rgba(25, 118, 210, 0.15);
}

.board-toolbar__button--active {
    border-color: rgba(25, 118, 210, 0.35);
    background: rgba(25, 118, 210, 0.08);
    color: #1976d2;
}

.board-toolbar__button--active:hover {
    background: rgba(25, 118, 210, 0.12);
}

.board-toolbar__count {
    min-width: 1.125rem;
    height: 1.125rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 0.3125rem;
    border-radius: 999px;
    background: #1976d2;
    color: #ffffff;
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    user-select: none;
    -webkit-user-select: none;
}

.board-toolbar__new-task {
    flex: 0 0 auto;
    border-radius: 0.5rem;
}

.board-toolbar__new-task :deep(.v-btn__content) {
    user-select: none;
}

.board-toolbar__search {
    flex: 0 1 17rem;
    min-width: 12rem;
    margin-right: 0.375rem;
}

:deep(.board-toolbar__search .v-field) {
    --v-field-border-opacity: 1;

    min-height: 2.375rem;
    border-radius: 0.625rem;
    background: rgb(var(--v-theme-surface));

    outline: none !important;

    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease;
}

:deep(.board-toolbar__search input),
:deep(.board-toolbar__search input:focus),
:deep(.board-toolbar__search input:focus-visible) {
    outline: none !important;
    box-shadow: none !important;
}

:deep(.board-toolbar__search .v-field__outline) {
    color: rgb(var(--v-theme-outline, 225, 228, 232));
}

:deep(.board-toolbar__search .v-field__outline__start),
:deep(.board-toolbar__search .v-field__outline__end) {
    border-color: currentColor;
    opacity: 1;
}

:deep(.board-toolbar__search .v-field__outline__notch)::before,
:deep(.board-toolbar__search .v-field__outline__notch)::after {
    border-color: currentColor;
}

:deep(.board-toolbar__search .v-field:hover .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 0.55;
}

:deep(.board-toolbar__search .v-field--focused) {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

:deep(.board-toolbar__search .v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

:deep(.board-toolbar__search .v-field__prepend-inner) {
    padding-inline-start: 0.75rem;
}

:deep(.board-toolbar__search .v-field__prepend-inner .v-icon) {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 1.125rem;
    opacity: 0.9;
    transition:
        color 0.15s ease,
        opacity 0.15s ease;
}

:deep(
    .board-toolbar__search .v-field--focused .v-field__prepend-inner .v-icon
) {
    color: rgb(var(--v-theme-primary));
    opacity: 1;
}

.board-toolbar__search-shortcut {
    display: inline-flex;
    align-items: center;
    gap: 0.1875rem;
    margin-right: 0.125rem;
    pointer-events: none;
}

.board-toolbar__search-shortcut kbd {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.25rem;
    height: 1.25rem;
    padding: 0 0.25rem;
    border: 1px solid rgb(var(--v-theme-outline, 225, 228, 232));
    border-radius: 0.3125rem;
    background: rgb(245, 246, 248);
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-family: inherit;
    font-size: 0.6875rem;
    font-weight: 600;
    line-height: 1;
    opacity: 0.85;
}
</style>
