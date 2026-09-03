<script setup>
/** @typedef {import("@/stores/taskboard.store").TaskboardRead} TaskboardRead */

defineProps({
    taskBoards: {
        /** @type {import('vue').PropType<TaskboardRead[]>} */
        type: Array,
        default: () => [],
    },
    unreadNotifications: {
        type: Number,
        default: 0,
    },
});

const emit = defineEmits(["toggle-rail", "new-board"]);

const mainNavItems = [
    {
        title: "Overview",
        value: "overview",
        routeName: "overview",
        icon: "mdi-view-dashboard-outline",
    },
    {
        title: "Projects",
        value: "projects",
        routeName: "projects",
        icon: "mdi-folder-outline",
    },
    {
        title: "Tasks",
        value: "tasks",
        icon: "mdi-checkbox-marked-circle-outline",
        isGroup: true,
    },
];

const secondaryNavItems = [
    {
        title: "Calendar",
        value: "calendar",
        routeName: "calendar",
        icon: "mdi-calendar-blank-outline",
    },
    {
        title: "Notifications",
        value: "notifications",
        routeName: "notifications",
        icon: "mdi-bell-outline",
        hasBadge: true,
    },
];

const footerNavItems = [
    {
        title: "Settings",
        value: "settings",
        routeName: "settings",
        icon: "mdi-cog-outline",
    },
];
</script>

<template>
    <v-navigation-drawer
        class="sidebar-drawer"
        elevation="0"
        width="240"
        rail-width="56"
    >
        <div class="sidebar-header">
            <div class="brand-container">
                <v-avatar size="1.625rem" rounded="auto" class="brand-avatar">
                    <v-icon
                        icon="mdi-layers-triple"
                        size="1.125rem"
                        color="primary"
                    />
                </v-avatar>
                <span class="brand-title">App</span>
            </div>
            <button
                type="button"
                class="rail-toggle-btn"
                aria-label="Toggle rail mode"
                @click="emit('toggle-rail')"
            >
                <v-icon icon="mdi-chevron-left" size="1.125rem" />
            </button>
        </div>

        <v-divider class="sidebar-divider" />

        <v-list density="compact" nav class="sidebar-list">
            <template v-for="item in mainNavItems" :key="item.value">
                <v-list-group
                    v-if="item.isGroup"
                    :value="item.value"
                    class="nav-group"
                >
                    <template #activator="{ props: groupProps }">
                        <v-list-item v-bind="groupProps" class="nav-item">
                            <template #prepend>
                                <v-icon :icon="item.icon" size="1.125rem" />
                            </template>
                            <v-list-item-title class="nav-title">
                                {{ item.title }}
                            </v-list-item-title>
                        </v-list-item>
                    </template>

                    <template v-if="taskBoards && taskBoards.length > 0">
                        <v-list-item
                            v-for="board in taskBoards"
                            :key="board.id"
                            :to="{ name: 'tasks', query: { board: board.id } }"
                            :value="`board-${board.id}`"
                            class="nav-item sub-item"
                        >
                            <template #prepend>
                                <v-icon
                                    :icon="
                                        board.icon || 'mdi-view-column-outline'
                                    "
                                    size="1rem"
                                    :style="{
                                        color:
                                            board.color ||
                                            'var(--v-theme-on-surface-variant)',
                                    }"
                                />
                            </template>

                            <v-list-item-title class="nav-title">
                                {{ board.name }}
                            </v-list-item-title>
                        </v-list-item>
                    </template>

                    <v-list-item
                        v-else
                        class="nav-item sub-item empty-boards-message"
                        disabled
                    >
                        <template #prepend>
                            <v-icon
                                icon="mdi-information-outline"
                                size="1rem"
                            />
                        </template>

                        <v-list-item-title class="nav-title">
                            No boards yet
                        </v-list-item-title>
                    </v-list-item>

                    <v-list-item
                        class="nav-item sub-item action-item"
                        @click="emit('new-board')"
                    >
                        <template #prepend>
                            <v-icon
                                icon="mdi-plus"
                                size="1rem"
                                class="text-primary"
                            />
                        </template>

                        <v-list-item-title
                            class="nav-title text-primary font-weight-semibold"
                        >
                            New Board
                        </v-list-item-title>
                    </v-list-item>
                </v-list-group>

                <v-list-item
                    v-else
                    :to="{ name: item.routeName }"
                    :value="item.value"
                    active-color="primary"
                    class="nav-item"
                >
                    <template #prepend>
                        <v-icon :icon="item.icon" size="1.125rem" />
                    </template>
                    <v-list-item-title class="nav-title">
                        {{ item.title }}
                    </v-list-item-title>
                </v-list-item>
            </template>

            <v-list-item
                v-for="item in secondaryNavItems"
                :key="item.value"
                :to="{ name: item.routeName }"
                :value="item.value"
                active-color="primary"
                class="nav-item"
            >
                <template #prepend>
                    <v-icon :icon="item.icon" size="1.125rem" />
                </template>
                <v-list-item-title class="nav-title">
                    {{ item.title }}
                </v-list-item-title>

                <template v-if="item.hasBadge" #append>
                    <span v-if="unreadNotifications > 0" class="unread-badge">
                        {{ unreadNotifications }}
                    </span>
                </template>
            </v-list-item>
        </v-list>

        <div class="sidebar-spacer" />
        <v-divider class="sidebar-divider" />

        <v-list density="compact" nav class="sidebar-list sidebar-footer">
            <v-list-item
                v-for="item in footerNavItems"
                :key="item.value"
                :to="{ name: item.routeName }"
                :value="item.value"
                active-color="primary"
                class="nav-item"
            >
                <template #prepend>
                    <v-icon :icon="item.icon" size="1.125rem" />
                </template>
                <v-list-item-title class="nav-title">
                    {{ item.title }}
                </v-list-item-title>
            </v-list-item>
        </v-list>

        <div class="resize-handle" />
    </v-navigation-drawer>
</template>

<style scoped>
.sidebar-drawer {
    background-color: var(--v-theme-surface, #ffffff);
    border-right: 0.0625rem solid var(--v-theme-outline, #e1e4e8);
    display: flex;
    flex-direction: column;
    height: 100%;
}

.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 3rem;
    padding: 0 0.75rem;
}

.brand-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    overflow: hidden;
}

.brand-avatar {
    background-color: rgba(var(--v-theme-primary, 25, 118, 210), 0.08);
    border: 0.0625rem solid rgba(var(--v-theme-primary, 25, 118, 210), 0.2);
    flex-shrink: 0;
}

.brand-title {
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--v-theme-on-surface, #1a1f2c);
    letter-spacing: -0.01em;
}

.rail-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.75rem;
    height: 1.75rem;
    border: 0.0625rem solid var(--v-theme-outline, #d0d5dd);
    border-radius: 0.375rem;
    background-color: var(--v-theme-surface, #ffffff);
    color: var(--v-theme-on-surface-variant, #475467);
    cursor: pointer;
    transition:
        border-color 0.15s ease,
        background-color 0.15s ease;
}

.rail-toggle-btn:hover {
    border-color: var(--v-theme-outline-dark, #98a2b3);
    background-color: var(--v-theme-surface-variant, #f8f9fa);
}

.sidebar-divider {
    border-color: var(--v-theme-outline, #e1e4e8);
    opacity: 1;
}

.sidebar-list {
    padding: 0.5rem 0.375rem;
}

.nav-item {
    min-height: 2rem;
    border-radius: 0.375rem;
    margin-bottom: 0.125rem;
    color: var(--v-theme-on-surface-variant, #344054);
}

.nav-item:hover {
    background-color: var(--v-theme-surface-variant, #f8f9fa);
}

.nav-title {
    font-size: 0.8125rem;
    font-weight: 500;
    letter-spacing: normal;
}

.sub-item {
    padding-left: 2.25rem;
}

.action-item {
    cursor: pointer;
}

.nav-subheader {
    font-size: 0.6875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--v-theme-on-surface-variant, #8c929d);
    height: 1.5rem;
    padding-left: 2.25rem;
    line-height: 1.5rem;
}

.project-dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    display: inline-block;
}

.unread-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.125rem;
    height: 1.125rem;
    padding: 0 0.25rem;
    border-radius: 0.5rem;
    font-size: 0.6875rem;
    font-weight: 700;
    background-color: rgba(var(--v-theme-primary, 25, 118, 210), 0.12);
    color: var(--v-theme-primary, #1976d2);
}

.sidebar-spacer {
    flex: 1;
}

.sidebar-footer {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
}

.resize-handle {
    position: absolute;
    top: 0;
    right: 0;
    width: 0.25rem;
    height: 100%;
    cursor: col-resize;
    transition: background-color 0.15s ease;
}

.resize-handle:hover {
    background-color: var(--v-theme-primary, #1976d2);
}
</style>
