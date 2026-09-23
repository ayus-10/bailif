<script setup>
import { computed, ref } from "vue";

const emit = defineEmits(["action", "new-task"]);

const searchQuery = ref("");
const activeFilterCount = ref(0);

const hasActiveFilters = computed(() => activeFilterCount.value > 0);

/**
 * @param {String} action
 */
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
                placeholder="Search tasks"
                prepend-inner-icon="mdi-magnify"
                density="compact"
                hide-details
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
                @click="handleAction('filter')"
            >
                <v-icon size="1rem"> mdi-filter-variant </v-icon>

                <span>Filter</span>

                <span v-if="activeFilterCount > 0" class="board-toolbar__count">
                    {{ activeFilterCount }}
                </span>
            </button>

            <button
                v-ripple
                type="button"
                class="board-toolbar__button"
                @click="handleAction('sort')"
            >
                <v-icon size="1rem"> mdi-sort-variant </v-icon>

                <span>Sort</span>
            </button>

            <button
                v-ripple
                type="button"
                class="board-toolbar__button"
                @click="handleAction('view')"
            >
                <v-icon size="1rem"> mdi-view-grid-outline </v-icon>

                <span>View</span>

                <v-icon size="0.875rem"> mdi-chevron-down </v-icon>
            </button>
        </div>

        <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            variant="flat"
            density="comfortable"
            class="text-none board-toolbar__new-task"
            @click="handleNewTask"
        >
            New task
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
    border-bottom: 0.0625rem solid rgb(var(--v-theme-outline-variant));
}

.board-toolbar__left {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex: 1 1 auto;
}

.board-toolbar__button {
    min-height: 2rem;
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0 0.75rem;
    border: none;
    border-radius: 0.5rem;
    background: transparent;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    font-weight: 500;
    line-height: 1rem;
    cursor: pointer;
    user-select: none;
    position: relative;
    overflow: hidden;
    isolation: isolate;
    transition:
        background-color 0.15s ease,
        color 0.15s ease;
}

.board-toolbar__button:hover {
    background: rgb(var(--v-theme-surface-light, 244, 245, 247));
    color: rgb(var(--v-theme-on-surface));
}

.board-toolbar__button:focus-visible {
    outline: 0.125rem solid rgb(var(--v-theme-primary));
    outline-offset: 0.125rem;
}

.board-toolbar__button--active {
    background: rgb(var(--v-theme-primary));
    color: rgb(var(--v-theme-on-primary, 255, 255, 255));
}

.board-toolbar__button--active:hover {
    background: rgb(var(--v-theme-primary-darken-1, 21, 101, 192));
}

.board-toolbar__count {
    min-width: 1.125rem;
    height: 1.125rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0 0.3125rem;
    border-radius: 999px;
    background: rgb(var(--v-theme-primary));
    color: #ffffff;
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    user-select: none;
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

    --search-border-resting: rgb(var(--v-theme-outline, 225, 228, 232));
    --search-border-hover: rgb(var(--v-theme-outline-variant));
    --search-border-focus: rgb(var(--v-theme-primary));
    --search-ring-focus: rgba(
        var(--v-theme-primary),
        var(--v-focus-opacity, 0.15)
    );
    --search-ring-hover: rgba(var(--v-theme-outline-variant), 0.5);
}

:deep(.board-toolbar__search .v-field) {
    min-height: 2.375rem;
    border-radius: 0.625rem;
    background: rgb(var(--v-theme-surface));
    outline: none;
    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        box-shadow 0.15s ease;
}

:deep(.board-toolbar__search input) {
    outline: none;
    box-shadow: none;
}

:deep(.board-toolbar__search .v-field__outline) {
    color: var(--search-border-resting);
    opacity: 1;
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
    color: rgb(var(--v-theme-outline-variant, 165, 172, 182)) !important;
    opacity: 1;
}

:deep(.board-toolbar__search .v-field:hover) {
    box-shadow: 0 0 0 0.0625rem var(--search-ring-hover);
}

:deep(.board-toolbar__search .v-field--focused .v-field__outline) {
    color: var(--search-border-focus);
    opacity: 1;
}

:deep(.board-toolbar__search .v-field--focused) {
    box-shadow: 0 0 0 0.0625rem var(--search-ring-focus);
}

:deep(.board-toolbar__search .v-field--focused:hover .v-field__outline) {
    color: var(--search-border-focus) !important;
    opacity: 1;
}

:deep(.board-toolbar__search .v-field--focused:hover) {
    box-shadow: 0 0 0 0.0625rem var(--search-ring-focus);
}

:deep(
    .board-toolbar__search .v-field--focused .v-field__prepend-inner .v-icon
) {
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
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-family: inherit;
    font-size: 0.6875rem;
    font-weight: 600;
    line-height: 1;
    opacity: 0.85;
}
</style>
