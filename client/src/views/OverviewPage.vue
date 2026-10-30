<script setup>
import { computed, onMounted } from "vue";
import DashboardMetrics from "@/components/dashboard/DashboardMetrics.vue";
import DashboardSection from "@/components/dashboard/DashboardSection.vue";
import DashboardTaskList from "@/components/dashboard/DashboardTaskList.vue";
import { useToast } from "@/composables/useToast";
import { DASHBOARD_SHORTCUTS } from "@/constants/dashboard";
import { STATUS_META } from "@/constants/tasks";
import { useDashboardStore } from "@/stores/dashboard.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/dashboard").DashboardMetric} DashboardMetric
 */

const dashboardStore = useDashboardStore();
const toast = useToast();

const dashboard = computed(() => dashboardStore.data);

const isLoading = computed(
    () => dashboardStore.status === "loading" && !dashboard.value
);

const hasError = computed(
    () => dashboardStore.status === "error" && !dashboard.value
);

/**
 * @type {import("vue").ComputedRef<DashboardMetric[]>}
 */
const metrics = computed(() => {
    if (!dashboard.value) return [];

    const { projects, tasks } = dashboard.value;

    return [
        {
            key: "projects",
            label: "Projects",
            value: projects.total,
            icon: "mdi-folder-outline",
            caption: `${projects.active} active`,
        },
        {
            key: "tasks",
            label: "Total tasks",
            value: tasks.total,
            icon: "mdi-checkbox-marked-circle-outline",
        },
        {
            key: "completed",
            label: "Completed",
            value: tasks.completed,
            icon: "mdi-check-circle-outline",
        },
        {
            key: "pending",
            label: "Pending",
            value: tasks.pending,
            icon: "mdi-progress-clock",
        },
        {
            key: "overdue",
            label: "Overdue",
            value: tasks.overdue,
            icon: "mdi-alert-circle-outline",
            isAlert: tasks.overdue > 0,
        },
    ];
});

const completionPercent = computed(() => {
    const tasks = dashboard.value?.tasks;

    return tasks?.total ? Math.round((tasks.completed / tasks.total) * 100) : 0;
});

function load() {
    dashboardStore.fetch().catch((err) => showApiError(err, toast));
}

onMounted(load);
</script>

<template>
    <v-container fluid class="overview-page">
        <div class="overview-page__header">
            <h1 class="text-h5 font-weight-medium">Overview</h1>

            <v-btn
                icon="mdi-refresh"
                variant="text"
                density="comfortable"
                aria-label="Refresh overview"
                :loading="dashboardStore.status === 'loading'"
                @click="load"
            />
        </div>

        <v-skeleton-loader
            v-if="isLoading"
            type="article, article"
            class="overview-page__skeleton"
        />

        <div v-else-if="hasError" class="overview-page__error">
            <v-icon icon="mdi-alert-circle-outline" size="32" />

            <p>We couldn't load your overview.</p>

            <v-btn
                color="primary"
                variant="flat"
                class="text-none"
                @click="load"
            >
                Try again
            </v-btn>
        </div>

        <template v-else-if="dashboard">
            <DashboardMetrics :metrics="metrics" />

            <div class="overview-page__grid">
                <DashboardSection
                    title="Upcoming deadlines"
                    icon="mdi-calendar-clock-outline"
                    :action-to="{ name: 'calendar' }"
                    action-label="Calendar"
                >
                    <DashboardTaskList
                        :tasks="dashboard.upcoming_deadlines"
                        date-field="due_date"
                        empty-icon="mdi-calendar-check-outline"
                        empty-title="No upcoming deadlines"
                    />
                </DashboardSection>

                <DashboardSection
                    title="Recent activity"
                    icon="mdi-history"
                >
                    <DashboardTaskList
                        :tasks="dashboard.recent_activity"
                        empty-icon="mdi-history"
                        empty-title="No recent activity"
                    />
                </DashboardSection>

                <DashboardSection
                    title="Task progress"
                    icon="mdi-chart-box-outline"
                >
                    <div class="overview-progress">
                        <div class="overview-progress__summary">
                            <span>{{ completionPercent }}% complete</span>

                            <span class="overview-progress__count">
                                {{ dashboard.tasks.completed }} of
                                {{ dashboard.tasks.total }} tasks
                            </span>
                        </div>

                        <v-progress-linear
                            :model-value="completionPercent"
                            color="success"
                            rounded
                            height="6"
                        />

                        <ul class="overview-progress__list">
                            <li
                                v-for="meta in STATUS_META"
                                :key="meta.status"
                                class="overview-progress__item"
                            >
                                <v-icon
                                    :icon="meta.icon"
                                    :color="meta.color.value"
                                    size="16"
                                />

                                <span>{{ meta.label }}</span>

                                <span class="overview-progress__count">
                                    {{ dashboard.tasks.by_status[meta.status] ?? 0 }}
                                </span>
                            </li>
                        </ul>
                    </div>
                </DashboardSection>

                <DashboardSection
                    title="Taskboards"
                    icon="mdi-grid-large"
                    :action-to="{ name: 'taskboards-all' }"
                >
                    <v-list
                        v-if="dashboard.taskboards.length"
                        density="compact"
                        class="overview-boards"
                    >
                        <v-list-item
                            v-for="board in dashboard.taskboards"
                            :key="board.public_id"
                            :to="{
                                name: 'taskboards',
                                params: { id: board.public_id },
                            }"
                            rounded="lg"
                        >
                            <template #prepend>
                                <v-icon
                                    icon="mdi-view-column-outline"
                                    size="16"
                                    :color="board.color || undefined"
                                />
                            </template>

                            <v-list-item-title class="overview-boards__title">
                                {{ board.name }}
                            </v-list-item-title>

                            <template #append>
                                <span class="overview-progress__count">
                                    {{ board.task_count }}
                                    {{ board.task_count === 1 ? "task" : "tasks" }}
                                </span>
                            </template>
                        </v-list-item>
                    </v-list>

                    <div v-else class="overview-page__empty">
                        <v-icon icon="mdi-view-column-outline" size="24" />

                        <span>No taskboards in the active project</span>
                    </div>
                </DashboardSection>
            </div>

            <DashboardSection title="Shortcuts" icon="mdi-lightning-bolt-outline">
                <div class="overview-shortcuts">
                    <v-btn
                        v-for="shortcut in DASHBOARD_SHORTCUTS"
                        :key="shortcut.routeName"
                        :to="{ name: shortcut.routeName }"
                        :prepend-icon="shortcut.icon"
                        variant="tonal"
                        color="primary"
                        class="text-none"
                    >
                        {{ shortcut.title }}
                    </v-btn>
                </div>
            </DashboardSection>
        </template>
    </v-container>
</template>

<style scoped>
.overview-page {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
}

.overview-page__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.overview-page__grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

.overview-page__error,
.overview-page__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2rem 1rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}

.overview-page__empty {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
}

.overview-progress {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0.5rem;
}

.overview-progress__summary {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    font-size: 0.8125rem;
    font-weight: 600;
}

.overview-progress__count {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
    font-weight: 400;
}

.overview-progress__list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.5rem 1rem;
    margin: 0;
    padding: 0;
    list-style: none;
}

.overview-progress__item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8125rem;
}

.overview-progress__item .overview-progress__count {
    margin-left: auto;
}

.overview-boards {
    padding: 0;
    background: transparent;
}

.overview-boards__title {
    font-size: 0.8125rem;
    font-weight: 500;
}

.overview-shortcuts {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.5rem;
}

@media (min-width: 960px) {
    .overview-page__grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
</style>
