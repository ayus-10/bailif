<script setup>
import { PRIORITY_META } from "@/constants/tasks";
import { formatDate } from "@/utils/dateFormatters";

/**
 * @typedef {import("@/types/dashboard").DashboardTaskRead} DashboardTaskRead
 */

const props = defineProps({
    tasks: {
        type: /** @type {import("vue").PropType<DashboardTaskRead[]>} */ (
            Array
        ),
        default: /** @returns {DashboardTaskRead[]} */ () => [],
    },
    dateField: {
        type: String,
        default: "updated_at",
    },
    emptyTitle: {
        type: String,
        required: true,
    },
    emptyIcon: {
        type: String,
        required: true,
    },
});

/**
 * @param {DashboardTaskRead} task
 */
function isOverdue(task) {
    return (
        props.dateField === "due_date" &&
        !!task.due_date &&
        new Date(task.due_date) < new Date()
    );
}

/**
 * @param {DashboardTaskRead} task
 */
function taskDate(task) {
    return props.dateField === "due_date" ? task.due_date : task.updated_at;
}
</script>

<template>
    <v-list v-if="tasks.length" density="compact" class="dashboard-task-list">
        <v-list-item
            v-for="task in tasks"
            :key="task.public_id"
            :to="{ name: 'task', params: { id: task.public_id } }"
            rounded="lg"
        >
            <template #prepend>
                <v-icon
                    :icon="PRIORITY_META[task.priority].icon"
                    :color="PRIORITY_META[task.priority].color"
                    size="14"
                />
            </template>

            <v-list-item-title class="dashboard-task-list__title">
                {{ task.title }}
            </v-list-item-title>

            <v-list-item-subtitle class="dashboard-task-list__project">
                {{ task.project_name }}
            </v-list-item-subtitle>

            <template #append>
                <span
                    class="dashboard-task-list__date"
                    :class="{
                        'dashboard-task-list__date--overdue': isOverdue(task),
                    }"
                >
                    {{ formatDate(taskDate(task)) }}
                </span>
            </template>
        </v-list-item>
    </v-list>

    <div v-else class="dashboard-task-list__empty">
        <v-icon :icon="emptyIcon" size="24" />

        <span>{{ emptyTitle }}</span>
    </div>
</template>

<style scoped>
.dashboard-task-list {
    padding: 0;
    background: transparent;
}

.dashboard-task-list__title {
    font-size: 0.8125rem;
    font-weight: 500;
}

.dashboard-task-list__project {
    font-size: 0.75rem;
}

.dashboard-task-list__date {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
    white-space: nowrap;
}

.dashboard-task-list__date--overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.dashboard-task-list__empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2rem 1rem;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.8125rem;
}
</style>
