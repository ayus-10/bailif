<template>
    <v-navigation-drawer
        v-model="isOpen"
        :rail="isRail"
        :width="drawerWidth"
        rail-width="72"
        permanent
        class="app-sidebar"
    >
        <div class="d-flex align-center px-2 py-3">
            <v-avatar color="primary" size="32" class="ml-1">
                <span class="text-subtitle-2 font-weight-bold">P</span>
            </v-avatar>
            <span
                v-if="!isRail"
                class="text-subtitle-1 font-weight-medium ml-3 text-truncate"
            >
                app
            </span>
            <v-spacer />
            <v-btn
                v-if="!isRail"
                icon="mdi-chevron-left"
                variant="text"
                size="small"
                @click="isRail = true"
            />
        </div>

        <v-btn
            v-if="isRail"
            icon="mdi-chevron-right"
            variant="text"
            size="small"
            class="d-block mx-auto mb-2"
            @click="isRail = false"
        />

        <v-divider />

        <v-list density="compact" nav>
            <v-list-item
                to="/dashboard"
                prepend-icon="mdi-view-dashboard-outline"
                title="Dashboard"
            />

            <v-list-group value="projects">
                <template #activator="{ props: activatorProps }">
                    <v-list-item
                        v-bind="activatorProps"
                        prepend-icon="mdi-folder-multiple-outline"
                        title="Projects"
                    />
                </template>
                <v-list-item
                    v-for="project in projects"
                    :key="project.id"
                    :to="`/projects/${project.id}`"
                    :prepend-icon="project.icon"
                    :title="project.name"
                    density="compact"
                />
            </v-list-group>

            <v-list-group value="tasks">
                <template #activator="{ props: activatorProps }">
                    <v-list-item
                        v-bind="activatorProps"
                        to="/tasks"
                        prepend-icon="mdi-checkbox-marked-outline"
                        title="Tasks"
                    />
                </template>

                <v-list-subheader v-if="!isRail">Status</v-list-subheader>
                <v-list-item
                    v-for="status in taskStatuses"
                    :key="status.value"
                    :active="taskFilters.status === status.value"
                    :prepend-icon="status.icon"
                    :title="status.label"
                    density="compact"
                    @click="setStatusFilter(status.value)"
                />

                <v-list-subheader v-if="!isRail">Priority</v-list-subheader>
                <v-list-item
                    v-for="priority in taskPriorities"
                    :key="priority.value"
                    :active="taskFilters.priority === priority.value"
                    density="compact"
                    @click="setPriorityFilter(priority.value)"
                >
                    <template #prepend>
                        <v-icon
                            :color="priority.color"
                            icon="mdi-flag"
                            size="small"
                        />
                    </template>
                    <v-list-item-title>{{ priority.label }}</v-list-item-title>
                </v-list-item>
            </v-list-group>

            <v-list-item
                to="/calendar"
                prepend-icon="mdi-calendar-blank-outline"
                title="Calendar"
            />

            <v-list-item
                to="/notifications"
                prepend-icon="mdi-bell-outline"
                title="Notifications"
            >
                <template #append>
                    <v-badge
                        v-if="unreadNotifications > 0"
                        :content="unreadNotifications"
                        color="error"
                        inline
                    />
                </template>
            </v-list-item>
        </v-list>

        <v-spacer />

        <v-divider />

        <v-list density="compact" nav>
            <v-list-item
                to="/settings"
                prepend-icon="mdi-cog-outline"
                title="Settings"
            />
        </v-list>

        <div v-if="!isRail" class="resize-handle" @mousedown="startResize" />
    </v-navigation-drawer>
</template>

<script setup>
import { useRouter } from "vue-router";
import { computed, onMounted, reactive, ref } from "vue";
import { taskPriorities, taskStatuses } from "@/constants/sidebarMeta";
import { useProjectsStore } from "@/stores/projects.store";

/** @typedef {import('@/types/task.js').TaskStatus} TaskStatusValue */
/** @typedef {import('@/types/task.js').TaskPriority} TaskPriorityValue */

/**
 * @typedef {Object} TaskFilters
 * @property {TaskStatusValue | null} status
 * @property {TaskPriorityValue | null} priority
 */

const router = useRouter();

const isOpen = ref(true);
const isRail = ref(false);
const unreadNotifications = ref(4);

const projectsStore = useProjectsStore();

onMounted(() => {
    projectsStore.fetch();
});

const projects = computed(() => projectsStore.items);

/** @type {TaskFilters} */
const taskFilters = reactive({
    status: null,
    priority: null,
});

/** @param {TaskStatusValue} value */
function setStatusFilter(value) {
    taskFilters.status = taskFilters.status === value ? null : value;
    router.push({ path: "/tasks", query: { ...taskFilters } });
}

/** @param {TaskPriorityValue} value */
function setPriorityFilter(value) {
    taskFilters.priority = taskFilters.priority === value ? null : value;
    router.push({ path: "/tasks", query: { ...taskFilters } });
}

const MIN_WIDTH = 220;
const MAX_WIDTH = 440;
const drawerWidth = ref(280);

let startX = 0;
let startWidth = 0;

/** @param {MouseEvent} event */
function startResize(event) {
    startX = event.clientX;
    startWidth = drawerWidth.value;
    window.addEventListener("mousemove", handleResize);
    window.addEventListener("mouseup", stopResize);
}

/** @param {MouseEvent} event */
function handleResize(event) {
    const delta = event.clientX - startX;
    const next = startWidth + delta;
    drawerWidth.value = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, next));
}

function stopResize() {
    window.removeEventListener("mousemove", handleResize);
    window.removeEventListener("mouseup", stopResize);
}
</script>

<style scoped>
.app-sidebar {
    display: flex;
    flex-direction: column;
    position: relative;
}

.resize-handle {
    position: absolute;
    top: 0;
    right: 0;
    width: 4px;
    height: 100%;
    cursor: col-resize;
    background: transparent;
}

.resize-handle:hover {
    background: rgba(var(--v-theme-primary), 0.4);
}
</style>
