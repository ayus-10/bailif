<script setup>
import { computed } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";
import {
    STATUS_META,
    TYPE_ICONS,
    TYPE_LABELS,
    FALLBACK_STATUS_META,
    FALLBACK_TYPE_ICON,
} from "@/constants/taskMeta";
import { formatDate, formatDuration, isTaskOverdue, parseTags } from "@/utils/taskFormatters";

/** @typedef {import('@/types/task').TaskRead} TaskRead */

const props = defineProps({
    task: {
        /** @type {import('vue').PropType<TaskRead>} */
        type: Object,
        required: true,
    },
});

defineEmits(["back", "edit"]);

const statusMeta = computed(
    () =>
        STATUS_META[props.task.status] ?? {
            ...FALLBACK_STATUS_META,
            label: props.task.status,
        }
);

const typeIcon = computed(() => TYPE_ICONS[props.task.type] ?? FALLBACK_TYPE_ICON);
const typeLabel = computed(() => TYPE_LABELS[props.task.type] ?? props.task.type);
const isOverdue = computed(() => isTaskOverdue(props.task));
const tags = computed(() => parseTags(props.task.tags));

// Rich-text-ready paragraph split: a blank line breaks a new paragraph, a
// single newline breaks a line within one (via `white-space: pre-wrap`).
// Swap this for a real renderer (markdown, Tiptap JSON, etc.) later without
// touching the surrounding `.prose` layout.
const descriptionParagraphs = computed(() =>
    (props.task.description ?? "")
        .split(/\n{2,}/)
        .map((p) => p.trim())
        .filter(Boolean)
);
</script>

<template>
    <div class="task-page">
        <div class="task-page__topbar">
            <v-btn
                icon="mdi-arrow-left"
                variant="text"
                density="comfortable"
                @click="$emit('back')"
            />

            <div v-if="task.project" class="task-page__crumb">
                <v-icon icon="mdi-folder-outline" size="14" />
                <span>{{ task.project.name }}</span>
            </div>

            <v-spacer />

            <v-btn variant="tonal" prepend-icon="mdi-pencil-outline" @click="$emit('edit')">
                Edit
            </v-btn>
        </div>

        <header class="task-page__header">
            <div class="task-page__eyebrow">
                <v-icon :icon="typeIcon" size="14" />
                <span>{{ typeLabel }}</span>
            </div>

            <h1 class="task-page__title">{{ task.title }}</h1>

            <div class="task-page__badges">
                <v-chip
                    size="small"
                    variant="tonal"
                    :color="statusMeta.color"
                    :prepend-icon="statusMeta.icon"
                >
                    {{ statusMeta.label }}
                </v-chip>

                <v-chip
                    size="small"
                    variant="flat"
                    :color="PRIORITY_COLORS[task.priority] ?? 'default'"
                >
                    {{ task.priority.toUpperCase() }} priority
                </v-chip>

                <span v-if="isOverdue" class="task-page__overdue-flag">
                    <v-icon icon="mdi-calendar-alert" size="14" />
                    Overdue
                </span>
            </div>
        </header>

        <div class="task-page__body">
            <main class="task-page__main">
                <section class="panel">
                    <h2 class="panel__label">Description</h2>

                    <div v-if="descriptionParagraphs.length" class="prose">
                        <p v-for="(para, i) in descriptionParagraphs" :key="i">{{ para }}</p>
                    </div>
                    <p v-else class="panel__empty">No description yet.</p>
                </section>

                <section class="panel panel--placeholder">
                    <h2 class="panel__label">Timeline</h2>

                    <div class="gantt-placeholder">
                        <v-icon icon="mdi-chart-gantt" size="26" />
                        <p>Related-task timeline is coming soon.</p>
                    </div>
                </section>
            </main>

            <aside class="task-page__sidebar">
                <div class="panel">
                    <h2 class="panel__label">Details</h2>

                    <dl class="detail-list">
                        <div class="detail-list__row">
                            <dt>Project</dt>
                            <dd>{{ task.project?.name ?? "—" }}</dd>
                        </div>
                        <div class="detail-list__row">
                            <dt>Start</dt>
                            <dd>{{ formatDate(task.start_date) ?? "—" }}</dd>
                        </div>
                        <div class="detail-list__row">
                            <dt>Due</dt>
                            <dd :class="{ overdue: isOverdue }">
                                {{ formatDate(task.due_date) ?? "—" }}
                            </dd>
                        </div>
                        <div class="detail-list__row">
                            <dt>Estimate</dt>
                            <dd>{{ formatDuration(task.estimated_duration_minutes) ?? "—" }}</dd>
                        </div>
                    </dl>
                </div>

                <div v-if="tags.length" class="panel">
                    <h2 class="panel__label">Tags</h2>
                    <div class="tag-list">
                        <v-chip v-for="tag in tags" :key="tag" size="small" variant="tonal">
                            {{ tag }}
                        </v-chip>
                    </div>
                </div>
            </aside>
        </div>
    </div>
</template>

<style scoped>
.task-page {
    max-width: 960px;
    margin: 0 auto;
    padding: 24px 20px 64px;
}

.task-page__topbar {
    display: flex;
    align-items: center;
    gap: 12px;
}

.task-page__crumb {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8125rem;
    color: rgba(var(--v-theme-on-surface), 0.65);
}

.task-page__header {
    padding: 20px 0 28px;
    margin-bottom: 28px;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.task-page__eyebrow {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.task-page__title {
    margin: 0 0 14px;
    font-size: 1.75rem;
    font-weight: 600;
    line-height: 1.25;
}

.task-page__badges {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.task-page__overdue-flag {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8125rem;
    font-weight: 600;
    color: rgb(var(--v-theme-error));
}

.task-page__body {
    display: grid;
    grid-template-columns: 1fr 280px;
    align-items: start;
    gap: 28px;
}

@media (max-width: 760px) {
    .task-page__body {
        grid-template-columns: 1fr;
    }
}

.task-page__main {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 0;
}

.task-page__sidebar {
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: sticky;
    top: 20px;
}

@media (max-width: 760px) {
    .task-page__sidebar {
        position: static;
    }
}

.panel {
    padding: 20px 22px;
    border: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-radius: 12px;
    background: rgb(var(--v-theme-surface));
}

.panel__label {
    margin: 0 0 14px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.panel__empty {
    margin: 0;
    font-size: 0.875rem;
    font-style: italic;
    color: rgba(var(--v-theme-on-surface), 0.5);
}

/* Rich-text-ready reading layout: capped measure, generous leading, and
   paragraph rhythm so a future markdown/HTML renderer drops in cleanly. */
.prose {
    max-width: 68ch;
    font-size: 0.9375rem;
    line-height: 1.7;
    color: rgba(var(--v-theme-on-surface), 0.87);
}

.prose p {
    margin: 0 0 1em;
    white-space: pre-wrap;
}

.prose p:last-child {
    margin-bottom: 0;
}

.panel--placeholder {
    background: transparent;
    border-style: dashed;
}

.gantt-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 28px 16px;
    color: rgba(var(--v-theme-on-surface), 0.4);
    text-align: center;
}

.gantt-placeholder p {
    margin: 0;
    font-size: 0.8125rem;
}

.detail-list {
    margin: 0;
}

.detail-list__row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 7px 0;
    font-size: 0.8125rem;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.06);
}

.detail-list__row:last-child {
    border-bottom: none;
}

.detail-list__row dt {
    color: rgba(var(--v-theme-on-surface), 0.55);
}

.detail-list__row dd {
    margin: 0;
    font-weight: 500;
    text-align: right;
}

.detail-list__row dd.overdue {
    color: rgb(var(--v-theme-error));
    font-weight: 600;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
</style>
