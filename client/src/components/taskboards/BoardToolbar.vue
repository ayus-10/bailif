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
            />

            <button
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
            density="compact"
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
    border-bottom: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
}

.board-toolbar__left {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.board-toolbar__search {
    width: 16rem;
    margin-right: 0.375rem;
}

.board-toolbar__button {
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

.board-toolbar__button:hover {
    border-color: var(--v-theme-outline, #e1e4e8);
    background: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface, #1a1f2c);
}

.board-toolbar__button--active {
    border-color: var(--v-theme-accent, #7c3aed);
    color: var(--v-theme-accent, #7c3aed);
}

.board-toolbar__count {
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

.board-toolbar__new-task {
    flex: 0 0 auto;
}

:deep(.board-toolbar__search .v-field) {
    --v-field-border-opacity: 1;
}

:deep(.board-toolbar__search .v-field__outline) {
    color: var(--v-theme-outline, #e1e4e8);
}

:deep(.board-toolbar__search .v-field--focused .v-field__outline) {
    color: var(--v-theme-primary, #1976d2);
}
</style>
