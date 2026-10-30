<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
import DashboardMetrics from "@/components/dashboard/DashboardMetrics.vue";
import DashboardSection from "@/components/dashboard/DashboardSection.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { PERMISSION_ITEMS, STATUS_ITEMS } from "@/constants/projects";
import { useProject, useProjectSummary } from "@/queries/projects.queries";
import { useAuthStore } from "@/stores/auth";
import { formatDate } from "@/utils/dateFormatters";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/dashboard").DashboardMetric} DashboardMetric
 */

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
});

const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const { projectId: activeProjectId } = useActiveProject();

const projectId = computed(() => Number(props.id));

const projectQuery = useProject(projectId);
const summaryQuery = useProjectSummary(projectId);
const project = computed(() => projectQuery.data.value ?? null);
const summary = computed(() => summaryQuery.data.value ?? null);

const isActive = computed(() => activeProjectId.value === projectId.value);

const isLoading = computed(
    () => projectQuery.isLoading.value || summaryQuery.isLoading.value
);

/**
 * @type {import("vue").ComputedRef<DashboardMetric[]>}
 */
const metrics = computed(() => {
    if (!summary.value) return [];

    const { tasks } = summary.value;

    return [
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

const details = computed(() => {
    if (!project.value) return [];

    const current = project.value;

    return [
        {
            label: "Status",
            value: STATUS_ITEMS.find((item) => item.value === current.status)
                ?.title,
        },
        { label: "Start", value: formatDate(current.start_date) },
        { label: "Target end", value: formatDate(current.target_end_date) },
        { label: "Actual end", value: formatDate(current.actual_end_date) },
        { label: "Timezone", value: current.timezone },
        {
            label: "Agent",
            value: current.agent_enabled
                ? PERMISSION_ITEMS.find(
                      (item) =>
                          item.value === current.default_agent_permission_level
                  )?.title
                : "Disabled",
        },
    ];
});

/**
 * @param {boolean} [forceRefresh]
 */
function load(forceRefresh = false) {
    Promise.all([projectQuery.refetch(), summaryQuery.refetch()]).catch((err) =>
        showApiError(err, toast)
    );
}

async function setActive() {
    try {
        await authStore.setActiveProject(projectId.value);
        toast.success("Active project updated");
    } catch (err) {
        showApiError(err, toast);
    }
}

/**
 * @param {string} action
 */
function handleNavigate(action) {
    if (action === "settings") {
        router.push({
            name: "project-settings",
            params: { id: projectId.value },
        });
    }
}
</script>

<template>
    <v-container fluid class="project-overview">
        <v-skeleton-loader v-if="isLoading" type="article, article" />

        <div v-else-if="!project" class="project-overview__message">
            <v-icon icon="mdi-alert-circle-outline" size="32" />

            <p>This project could not be loaded.</p>

            <div class="d-flex ga-2">
                <v-btn
                    variant="text"
                    class="text-none"
                    :to="{ name: 'project-list' }"
                >
                    Back to projects
                </v-btn>

                <v-btn
                    color="primary"
                    variant="flat"
                    class="text-none"
                    @click="load(true)"
                >
                    Try again
                </v-btn>
            </div>
        </div>

        <template v-else>
            <ProjectHeader :project="project" @navigate="handleNavigate" />

            <div class="project-overview__actions">
                <v-chip v-if="isActive" color="primary" variant="tonal">
                    Active project
                </v-chip>

                <v-btn
                    v-else
                    color="primary"
                    variant="tonal"
                    class="text-none"
                    @click="setActive"
                >
                    Set as active
                </v-btn>
            </div>

            <DashboardMetrics :metrics="metrics" />

            <div class="project-overview__grid">
                <DashboardSection
                    title="Details"
                    icon="mdi-information-outline"
                >
                    <dl class="project-overview__details">
                        <div
                            v-for="detail in details"
                            :key="detail.label"
                            class="project-overview__detail"
                        >
                            <dt>{{ detail.label }}</dt>

                            <dd>{{ detail.value || "Not set" }}</dd>
                        </div>
                    </dl>
                </DashboardSection>

                <DashboardSection title="Taskboards" icon="mdi-grid-large">
                    <v-list
                        v-if="summary?.taskboards.length"
                        density="compact"
                        class="project-overview__boards"
                    >
                        <v-list-item
                            v-for="board in summary.taskboards"
                            :key="board.public_id"
                            :to="
                                isActive
                                    ? {
                                          name: 'taskboards',
                                          params: { id: board.public_id },
                                      }
                                    : undefined
                            "
                            :title="board.name"
                            :subtitle="`${board.task_count} ${board.task_count === 1 ? 'task' : 'tasks'}`"
                            rounded="lg"
                        >
                            <template #prepend>
                                <v-icon
                                    icon="mdi-view-column-outline"
                                    size="16"
                                    :color="board.color || undefined"
                                />
                            </template>
                        </v-list-item>
                    </v-list>

                    <div v-else class="project-overview__message">
                        <v-icon icon="mdi-view-column-outline" size="24" />

                        <span>No taskboards in this project</span>
                    </div>
                </DashboardSection>
            </div>
        </template>
    </v-container>
</template>

<style scoped>
.project-overview {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
}

.project-overview__actions {
    display: flex;
    align-items: center;
}

.project-overview__grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

.project-overview__message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2rem 1rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}

.project-overview__details {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem 1rem;
    margin: 0;
    padding: 0.5rem;
}

.project-overview__detail dt {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
}

.project-overview__detail dd {
    margin: 0;
    font-size: 0.8125rem;
    font-weight: 500;
}

.project-overview__boards {
    padding: 0;
    background: transparent;
}

@media (min-width: 960px) {
    .project-overview__grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
</style>
