<script setup>
import { computed } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";
import {
    STATUS_META,
    TYPE_ICONS,
    FALLBACK_STATUS_META,
    FALLBACK_TYPE_ICON,
} from "@/constants/taskMeta";
import { formatDate, isTaskOverdue, parseTags } from "@/utils/taskFormatters";
import { useRouter } from "vue-router";
import { htmlPreview } from "@/utils/htmlFormatters";

/** @typedef {import('@/types/task').TaskRead} TaskRead */

const props = defineProps({
    task: {
        /** @type {import('vue').PropType<TaskRead>} */
        type: Object,
        required: true,
    },
});

const statusMeta = computed(
    () =>
        STATUS_META[props.task.status] ?? {
            ...FALLBACK_STATUS_META,
            label: props.task.status,
        }
);

const router = useRouter();

const typeIcon = computed(
    () => TYPE_ICONS[props.task.type] ?? FALLBACK_TYPE_ICON
);
const isOverdue = computed(() => isTaskOverdue(props.task));
const tagCount = computed(() => parseTags(props.task.tags).length);
</script>
<template>
    <v-card
        variant="outlined"
        rounded="lg"
        class="task-row"
        :class="{ 'task-row--overdue': isOverdue }"
        ripple
        link
        @click="router.push(`/tasks/${task.id}`)"
    >
        <div class="status-rail" :class="`bg-${statusMeta.color}`" />

        <v-tooltip :text="statusMeta.label" location="top" open-delay="300">
            <template #activator="{ props: tip }">
                <v-icon
                    v-bind="tip"
                    :icon="typeIcon"
                    size="16"
                    :color="statusMeta.color"
                    class="task-row__type"
                />
            </template>
        </v-tooltip>

        <div class="task-row__body">
            <div class="task-row__main">
                <span class="task-row__title text-body-2 font-weight-medium">
                    {{ task.title }}
                </span>
                <div class="task-row__spacer" />
                <div v-if="tagCount" class="task-row__meta">
                    <v-icon icon="mdi-tag-outline" size="12" />
                    <span>{{ tagCount }}</span>
                </div>
                <div
                    v-if="task.estimated_duration_minutes"
                    class="task-row__meta"
                >
                    <v-icon icon="mdi-timer-outline" size="12" />
                </div>
                <div
                    v-if="task.due_date"
                    class="task-row__meta"
                    :class="{ overdue: isOverdue }"
                >
                    <v-icon
                        :icon="
                            isOverdue
                                ? 'mdi-calendar-alert'
                                : 'mdi-calendar-blank-outline'
                        "
                        size="12"
                    />
                    <span>{{ formatDate(task.due_date) }}</span>
                </div>
                <v-chip
                    size="x-small"
                    variant="flat"
                    class="task-row__priority"
                    :color="PRIORITY_COLORS[task.priority] ?? 'default'"
                >
                    {{ task.priority.toUpperCase() }}
                </v-chip>
            </div>

            <p
                v-if="task.description"
                class="task-row__description text-caption"
            >
                {{ htmlPreview(task.description) }}
            </p>
        </div>
    </v-card>
</template>

<style scoped>
.task-row {
    position: relative;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: start;
    column-gap: 10px;
    padding: 10px 12px 10px 16px;
    overflow: hidden;
    cursor: pointer;
    user-select: none;
    transition:
        background-color 0.12s ease,
        transform 0.12s ease;
}

.task-row:hover {
    background-color: rgba(var(--v-theme-on-surface), 0.035);
}

.task-row:active {
    transform: scale(0.997);
}

.status-rail {
    position: absolute;
    inset: 0 auto 0 0;
    width: 3px;
}

.task-row__type {
    flex-shrink: 0;
    margin-top: 2px;
}

.task-row__body {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.task-row__main {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 20px;
}

.task-row__title {
    flex-shrink: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.task-row__spacer {
    flex: 1 1 auto;
}

.task-row__meta {
    display: flex;
    align-items: center;
    gap: 3px;
    flex-shrink: 0;
    font-size: 0.6875rem;
    color: rgba(var(--v-theme-on-surface), 0.6);
}

.task-row__meta.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.task-row__priority {
    flex-shrink: 0;
}

.task-row__description {
    margin: 0;
    color: rgba(var(--v-theme-on-surface), 0.6);
    display: -webkit-box;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
}

.task-row--overdue {
    border-color: rgba(var(--v-theme-error), 0.4);
}

@media (max-width: 520px) {
    .task-row__meta:not(:last-of-type) {
        display: none;
    }
}
</style>
