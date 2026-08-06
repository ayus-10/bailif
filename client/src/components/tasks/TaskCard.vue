<script setup>
import { computed } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";
/** @typedef {import('@/types/task').TaskRead} TaskRead */

const props = defineProps({
    task: {
        /** @type {import('vue').PropType<TaskRead>} */
        type: Object,
        required: true,
    },
});

const STATUS_META = {
    open: { color: "grey", icon: "mdi-circle-outline", label: "Open" },
    in_progress: {
        color: "blue",
        icon: "mdi-progress-clock",
        label: "In progress",
    },
    in_review: { color: "purple", icon: "mdi-eye-outline", label: "In review" },
    done: { color: "success", icon: "mdi-check-circle", label: "Done" },
    blocked: { color: "error", icon: "mdi-block-helper", label: "Blocked" },
    cancelled: {
        color: "grey-darken-1",
        icon: "mdi-close-circle-outline",
        label: "Cancelled",
    },
};

const TYPE_ICONS = {
    bug: "mdi-bug-outline",
    feature: "mdi-star-outline",
    task: "mdi-checkbox-marked-circle-outline",
    chore: "mdi-broom",
    epic: "mdi-flag-outline",
};

const statusMeta = computed(
    () =>
        STATUS_META[props.task.status] ?? {
            color: "grey",
            icon: "mdi-help-circle-outline",
            label: props.task.status,
        }
);

const typeIcon = computed(
    () => TYPE_ICONS[props.task.type] ?? "mdi-checkbox-blank-circle-outline"
);

const tags = computed(() =>
    (props.task.tags ?? "")
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean)
);

const isOverdue = computed(() => {
    if (!props.task.due_date) return false;
    if (["done", "cancelled"].includes(props.task.status)) return false;
    return new Date(props.task.due_date) < new Date();
});

/** @param {string} iso */
function formatDate(iso) {
    if (!iso) return null;
    return new Date(iso).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
    });
}

/** @param {number} minutes */
function formatDuration(minutes) {
    if (!minutes) return null;
    if (minutes < 60) return `${minutes}m`;
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return m ? `${h}h ${m}m` : `${h}h`;
}
</script>

<template>
    <v-card
        variant="outlined"
        rounded="lg"
        class="task-card"
        :class="{ 'task-card--overdue': isOverdue }"
        ripple
        link
    >
        <div class="status-rail" :class="`bg-${statusMeta.color}`" />

        <div class="pa-4 pl-5">
            <div class="d-flex align-start ga-3 mb-3">
                <v-avatar
                    size="32"
                    :color="statusMeta.color"
                    variant="tonal"
                    class="flex-shrink-0"
                >
                    <v-icon :icon="typeIcon" size="16" />
                </v-avatar>

                <div class="flex-grow-1 min-width-0">
                    <div class="text-subtitle-2 font-weight-medium">
                        {{ task.title }}
                    </div>

                    <div
                        v-if="task.description"
                        class="text-caption text-medium-emphasis mt-1"
                    >
                        {{ task.description }}
                    </div>
                </div>

                <v-chip
                    link
                    ripple
                    size="small"
                    variant="flat"
                    class="flex-shrink-0"
                    :color="PRIORITY_COLORS[task.priority] ?? 'default'"
                >
                    {{ task.priority.toUpperCase() }}
                </v-chip>
            </div>

            <div v-if="tags.length" class="d-flex flex-wrap ga-2 mb-3">
                <v-chip
                    v-for="tag in tags"
                    :key="tag"
                    link
                    ripple
                    size="x-small"
                    variant="tonal"
                >
                    {{ tag }}
                </v-chip>
            </div>

            <v-divider class="mb-3" />

            <div class="task-meta">
                <v-chip
                    link
                    ripple
                    size="x-small"
                    variant="tonal"
                    :color="statusMeta.color"
                    :prepend-icon="statusMeta.icon"
                >
                    {{ statusMeta.label }}
                </v-chip>

                <div v-if="task.project" class="meta-item">
                    <v-icon icon="mdi-folder-outline" size="14" />
                    <span>{{ task.project.name }}</span>
                </div>

                <div v-if="task.estimated_duration_minutes" class="meta-item">
                    <v-icon icon="mdi-timer-outline" size="14" />
                    <span>{{
                        formatDuration(task.estimated_duration_minutes)
                    }}</span>
                </div>

                <div v-if="task.start_date" class="meta-item">
                    <v-icon icon="mdi-calendar-start-outline" size="14" />
                    <span>{{ formatDate(task.start_date) }}</span>
                </div>

                <div
                    v-if="task.due_date"
                    class="meta-item"
                    :class="{ overdue: isOverdue }"
                >
                    <v-icon
                        :icon="
                            isOverdue
                                ? 'mdi-calendar-alert'
                                : 'mdi-calendar-blank-outline'
                        "
                        size="14"
                    />

                    <span>{{ formatDate(task.due_date) }}</span>
                </div>
            </div>
        </div>
    </v-card>
</template>

<style scoped>
.task-card {
    position: relative;
    overflow: hidden;
    cursor: pointer;
    user-select: none;

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.task-card:active {
    transform: translateY(0);
}

.status-rail {
    position: absolute;
    inset: 0 auto 0 0;
    width: 4px;
}

.task-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
    font-size: 0.75rem;
    color: rgba(var(--v-theme-on-surface), 0.65);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 4px;
}

.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.task-card--overdue {
    border-color: rgba(var(--v-theme-on-surface), 0.3);
}

.min-width-0 {
    min-width: 0;
}
</style>
