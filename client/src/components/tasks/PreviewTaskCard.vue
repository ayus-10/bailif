<script setup>
import { computed } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";
import { htmlPreview } from "@/utils/htmlFormatters";
import { formatDate, parseTags } from "@/utils/taskFormatters";

/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 */

const props = defineProps({
    task: {
        /**
         * @type {import("vue").PropType<TaskRead>}
         */
        type: Object,
        required: true,
    },

    accentColor: {
        type: String,
        default: "rgb(var(--v-theme-primary))",
    },
});

// TODO: TaskRead doesn't define `progress` yet
const progressValue = 67;

const tagCount = computed(() => parseTags(props.task.tags).length);
</script>

<template>
    <v-card
        variant="outlined"
        rounded="lg"
        class="preview-task-card"
        :style="{ '--task-accent': accentColor }"
        aria-hidden="true"
    >
        <div class="preview-task-card__top">
            <v-chip
                size="x-small"
                variant="tonal"
                class="preview-task-card__priority"
                :color="PRIORITY_COLORS[task.priority]"
            >
                {{ task.priority.toUpperCase() }}
            </v-chip>

            <span v-if="task.due_date" class="preview-task-card__date">
                <v-icon icon="mdi-calendar-blank-outline" size="12" />
                {{ formatDate(task.due_date) }}
            </span>
        </div>

        <h3 class="preview-task-card__title">
            {{ task.title }}
        </h3>

        <p v-if="task.description" class="task-card__description">
            {{ htmlPreview(task.description) }}
        </p>

        <div class="preview-task-card__progress-row">
            <span>Progress</span>
            <span>{{ progressValue }}%</span>
        </div>

        <div class="preview-task-card__progress-track">
            <div
                class="preview-task-card__progress-fill"
                :style="{ width: `${progressValue}%` }"
            />
        </div>

        <div class="preview-task-card__footer">
            <span v-if="tagCount" class="preview-task-card__meta">
                <v-icon icon="mdi-tag-outline" size="12" />
                {{ tagCount }}
            </span>

            <span v-if="task.status" class="preview-task-card__status">
                {{ task.status }}
            </span>
        </div>
    </v-card>
</template>

<style scoped>
.preview-task-card {
    --task-accent: rgb(var(--v-theme-primary));

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem 0.875rem;
    overflow: hidden;
    pointer-events: none;
    user-select: none;
    background: rgb(var(--v-theme-surface));
    border-color: rgb(var(--v-theme-outline-variant, 234, 236, 240));
    opacity: 0.58;
    filter: saturate(0.55);
}

.preview-task-card::after {
    position: absolute;
    inset: 0;
    content: "";
    pointer-events: none;
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.24),
        rgba(255, 255, 255, 0.04)
    );
}

.preview-task-card__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
}

.preview-task-card__priority {
    padding: 0.125rem 0.375rem;
    border: 0.0625rem solid currentColor;
    border-radius: 0.125rem;
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    letter-spacing: 0.05em;
}

.preview-task-card__date,
.preview-task-card__meta,
.preview-task-card__status {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.6875rem;
    white-space: nowrap;
}

.preview-task-card__title {
    margin: 0;
    overflow: hidden;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    line-height: 1.25rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.preview-task-card__description {
    display: -webkit-box;
    margin: 0;
    overflow: hidden;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    line-height: 1.35rem;
    -webkit-box-orient: vertical;
    line-clamp: 2;
}

.preview-task-card__progress-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.125rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.75rem;
    font-weight: 600;
}

.preview-task-card__progress-row span:last-child {
    color: rgb(var(--v-theme-on-surface));
    font-variant-numeric: tabular-nums;
}

.preview-task-card__progress-track {
    width: 100%;
    height: 0.375rem;
    overflow: hidden;
    border-radius: 999px;
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
}

.preview-task-card__progress-fill {
    height: 100%;
    border-radius: inherit;
    background: var(--task-accent);
}

.preview-task-card__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 1rem;
}
</style>
