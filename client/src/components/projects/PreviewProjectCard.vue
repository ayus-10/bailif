<script setup>
import { computed } from "vue";
import { formatDate } from "@/utils/dateFormatters";

/**
 * @typedef {import("@/types/project").ProjectRead} ProjectTemplate
 */

const props = defineProps({
    project: {
        /**
         * @type {import("vue").PropType<ProjectTemplate>}
         */
        type: Object,
        required: true,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["select"]);

const scheduleLabel = computed(() => {
    const start = formatDate(props.project.start_date);
    const end = formatDate(props.project.target_end_date);

    if (start && end) return `${start} – ${end}`;
    if (start) return `Starts ${start}`;
    if (end) return `Due ${end}`;
    return "No schedule set";
});

function onSelect() {
    if (props.disabled) return;
    emit("select");
}
</script>

<template>
    <button
        type="button"
        class="preview-project-card"
        :disabled="disabled"
        @click="onSelect"
    >
        <span class="preview-project-card__top">
            <span class="preview-project-card__identity">
                <span
                    class="preview-project-card__icon"
                    :style="
                        project.color
                            ? {
                                  color: project.color,
                                  backgroundColor: `color-mix(in srgb, ${project.color} 10%, rgb(var(--v-theme-surface)))`,
                              }
                            : undefined
                    "
                    aria-hidden="true"
                >
                    <v-icon
                        :icon="project.icon || 'mdi-folder-outline'"
                        size="18"
                    />
                </span>

                <span class="preview-project-card__heading">
                    <span class="preview-project-card__title">
                        {{ project.name }}
                    </span>

                    <span
                        v-if="project.description"
                        class="preview-project-card__description"
                    >
                        {{ project.description }}
                    </span>
                </span>
            </span>

            <span class="preview-project-card__use">Use</span>
        </span>

        <span class="preview-project-card__footer">
            <span class="preview-project-card__schedule">
                <v-icon
                    icon="mdi-calendar-range-outline"
                    size="14"
                    aria-hidden="true"
                />
                {{ scheduleLabel }}
            </span>
            <span v-if="project.status" class="preview-project-card__status">
                <span class="preview-project-card__status-label">Status</span>
                <span
                    class="preview-project-card__meta-separator"
                    aria-hidden="true"
                />
                {{ project.status }}
            </span>
        </span>
    </button>
</template>

<style scoped>
.preview-project-card {
    --project-accent: rgb(var(--v-theme-primary));

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    width: 100%;
    padding: 1rem;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
    color: inherit;
    cursor: pointer;
    text-align: left;
    user-select: none;
    -webkit-user-select: none;
    transition:
        border-color 0.12s ease,
        background-color 0.12s ease;
}

.preview-project-card + .preview-project-card {
    margin-top: 0.5rem;
}

.preview-project-card:hover:not(:disabled) {
    border-color: color-mix(
        in srgb,
        var(--project-accent) 22%,
        rgb(var(--v-theme-outline-variant, 234, 236, 240))
    );
    background-color: color-mix(
        in srgb,
        var(--project-accent) 3%,
        rgb(var(--v-theme-surface))
    );
}

.preview-project-card:focus {
    outline: none;
}

.preview-project-card:focus-visible {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

.preview-project-card:disabled {
    cursor: not-allowed;
    opacity: 0.55;
}

.preview-project-card__top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
    min-width: 0;
}

.preview-project-card__identity {
    display: flex;
    align-items: flex-start;
    min-width: 0;
    flex: 1 1 auto;
    gap: 0.625rem;
}

.preview-project-card__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    border-radius: 0.5rem;
    background: color-mix(
        in srgb,
        var(--project-accent) 10%,
        rgb(var(--v-theme-surface))
    );
    color: var(--project-accent);
}

.preview-project-card__heading {
    display: flex;
    flex-direction: column;
    min-width: 0;
    flex: 1 1 auto;
    gap: 0.125rem;
}

.preview-project-card__title {
    min-width: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.preview-project-card__description {
    min-width: 0;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.75rem;
    font-weight: 400;
    line-height: 1.1rem;
    display: -webkit-box;
    line-clamp: 2;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.preview-project-card__status {
    flex: 0 0 auto;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.75rem;
    font-weight: 500;
    line-height: 1rem;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.preview-project-card__footer {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding-top: 0.5rem;
    border-top: 0.0625rem solid
        rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.preview-project-card__schedule {
    display: flex;
    align-items: center;
    gap: 0.3125rem;
    min-width: 0;
    flex: 1 1 auto;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
    font-weight: 500;
    line-height: 1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.preview-project-card__use {
    flex: 0 0 auto;
    color: rgb(var(--v-theme-primary));
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    opacity: 0;
    transition: opacity 0.12s ease;
}

.preview-project-card__status-label {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-weight: 400;
}

.preview-project-card__meta-separator {
    width: 0.125rem;
    height: 0.125rem;
    flex: 0 0 auto;
    border-radius: 50%;
    background: rgb(var(--v-theme-text-disabled, 148, 157, 173));
}

.preview-project-card:hover:not(:disabled) .preview-project-card__use,
.preview-project-card:focus-visible .preview-project-card__use {
    opacity: 1;
}
</style>
