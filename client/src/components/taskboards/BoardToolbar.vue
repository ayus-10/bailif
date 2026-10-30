<script setup>
import { computed } from "vue";
import { PRIORITY_META, STATUS_META } from "@/constants/tasks";

const props = defineProps({
    search: {
        type: String,
        default: "",
    },
    status: {
        type: String,
        default: null,
    },
    priority: {
        type: String,
        default: null,
    },
});

const emit = defineEmits([
    "update:search",
    "update:status",
    "update:priority",
    "new-task",
]);

const statusItems = STATUS_META.map((meta) => ({
    title: meta.label,
    value: meta.status,
}));

const priorityItems = Object.entries(PRIORITY_META).map(([value, meta]) => ({
    title: meta.label,
    value,
}));

const activeFilterCount = computed(
    () => Number(!!props.status) + Number(!!props.priority)
);

const hasActiveFilters = computed(() => activeFilterCount.value > 0);

function handleNewTask() {
    emit("new-task");
}
</script>

<template>
    <div class="board-toolbar">
        <div class="board-toolbar__left">
            <v-text-field
                :model-value="search"
                placeholder="Search tasks"
                prepend-inner-icon="mdi-magnify"
                density="compact"
                hide-details
                clearable
                persistent-placeholder
                variant="outlined"
                class="board-toolbar__search"
                @update:model-value="emit('update:search', $event ?? '')"
            />

            <v-menu :close-on-content-click="false" location="bottom start">
                <template #activator="{ props: menuProps }">
                    <button
                        v-bind="menuProps"
                        v-ripple
                        type="button"
                        class="board-toolbar__button"
                        :class="{
                            'board-toolbar__button--active': hasActiveFilters,
                        }"
                    >
                        <v-icon size="1rem"> mdi-filter-variant </v-icon>

                        <span>Filter</span>

                        <span
                            v-if="activeFilterCount > 0"
                            class="board-toolbar__count"
                        >
                            {{ activeFilterCount }}
                        </span>
                    </button>
                </template>

                <v-card class="board-toolbar__filters" variant="outlined">
                    <v-select
                        :model-value="status"
                        class="board-toolbar__select"
                        :items="statusItems"
                        label="Status"
                        density="compact"
                        variant="outlined"
                        clearable
                        persistent-placeholder
                        hide-details
                        @update:model-value="emit('update:status', $event)"
                    />

                    <v-select
                        :model-value="priority"
                        class="board-toolbar__select"
                        :items="priorityItems"
                        label="Priority"
                        density="compact"
                        variant="outlined"
                        clearable
                        persistent-placeholder
                        hide-details
                        @update:model-value="emit('update:priority', $event)"
                    />
                </v-card>
            </v-menu>
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

.board-toolbar__filters {
    background-color: #fff;
    border: 1px solid rgb(var(--v-theme-outline, 225, 228, 232));
    border-radius: 0.5rem;
    box-shadow: none;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0.75rem;
}

.board-toolbar__select {
    min-width: 14rem;
}

:deep(.v-field) {
    background-color: #fff;
    border-radius: 0.375rem;
}

:deep(.v-field--outlined .v-field__outline) {
    --v-field-border-opacity: 1;
    color: #d0d5dd;
}

:deep(.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
}
</style>
