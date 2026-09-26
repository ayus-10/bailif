<script setup>
/**
 * @typedef {import("@/types/project").ProjectRead} ProjectRead
 */

/**
 * @typedef {Object} ProjectHeaderProps
 * @property {ProjectRead|null} [project]
 * @property {string} [title]
 * @property {string} [description]
 * @property {boolean} [showNewProject]
 */

/**
 * @type {ProjectHeaderProps}
 */
const props = defineProps({
    project: {
        /**
         * @type {import("vue").PropType<ProjectRead | null>}
         */
        type: Object,
        default: null,
    },
    title: {
        type: String,
        default: "Projects",
    },
    description: {
        type: String,
        default: "Manage projects and switch between your workspaces.",
    },
    showNewProject: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["navigate"]);

/**
 * * @param {string} action
 */
function handleNavigate(action) {
    emit("navigate", action);
}
</script>

<template>
    <header class="project-header">
        <div class="project-header__identity">
            <div
                v-if="props.project"
                class="project-header__icon"
                :style="{
                    '--project-accent': props.project.color || '#6366F1',
                }"
                aria-hidden="true"
            >
                <v-icon
                    :icon="props.project.icon || 'mdi-folder-outline'"
                    size="1.125rem"
                />
            </div>

            <div class="project-header__identity-content">
                <div class="project-header__title-row">
                    <h1 class="project-header__title">
                        {{ props.project?.name || props.title }}
                    </h1>

                    <span
                        v-if="props.project?.status"
                        class="project-header__status"
                    >
                        {{ props.project.status }}
                    </span>
                </div>

                <p class="project-header__description">
                    {{ props.project?.description || props.description }}
                </p>
            </div>
        </div>

        <div class="project-header__actions">
            <template v-if="props.project">
                <button
                    v-ripple
                    type="button"
                    class="project-header__icon-button"
                    aria-label="Project settings"
                    @click="() => handleNavigate('settings')"
                >
                    <v-icon size="1.125rem"> mdi-cog-outline </v-icon>
                </button>

                <button
                    v-ripple
                    type="button"
                    class="project-header__icon-button"
                    aria-label="Project members"
                    @click="() => handleNavigate('members')"
                >
                    <v-icon size="1.125rem"> mdi-account-group-outline </v-icon>
                </button>
            </template>

            <v-btn
                v-if="props.showNewProject"
                color="primary"
                prepend-icon="mdi-plus"
                variant="flat"
                density="comfortable"
                class="text-none project-header__new-project"
                @click="() => handleNavigate('project-new')"
            >
                New project
            </v-btn>
        </div>
    </header>
</template>

<style scoped>
.project-header {
    flex: 0 0 auto;
    min-height: 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
}

.project-header__identity {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.625rem;
}

.project-header__icon {
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0.0625rem solid
        color-mix(
            in srgb,
            var(--project-accent) 20%,
            var(--v-theme-outline-variant, #eaecf0)
        );
    border-radius: 0.375rem;
    background: color-mix(
        in srgb,
        var(--project-accent) 8%,
        var(--v-theme-surface, #ffffff)
    );
    color: var(--project-accent);
}

.project-header__identity-content {
    min-width: 0;
}

.project-header__title-row {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.project-header__title {
    margin: 0;
    overflow: hidden;
    color: var(--v-theme-on-surface, #1a1f2c);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.project-header__status {
    flex: 0 0 auto;
    padding: 0.125rem 0.375rem;
    border: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
    border-radius: 0.125rem;
    color: var(--v-theme-text-secondary, #475467);
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    user-select: none;
    -webkit-user-select: none;
}

.project-header__description {
    margin: 0.125rem 0 0;
    overflow: hidden;
    color: var(--v-theme-text-secondary, #475467);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.project-header__actions {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.project-header__icon-button {
    width: 2rem;
    height: 2rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: 0.0625rem solid transparent;
    border-radius: 0.375rem;
    background: transparent;
    color: var(--v-theme-text-secondary, #475467);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    isolation: isolate;
    transition: color 0.15s ease;
}

.project-header__icon-button:hover {
    color: rgb(var(--v-theme-primary));
}

.project-header__icon-button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

.project-header__new-project {
    flex: 0 0 auto;
    border-radius: 0.5rem;
}

.project-header__new-project :deep(.v-btn__content) {
    user-select: none;
}

@media (max-width: 48rem) {
    .project-header {
        align-items: flex-start;
    }

    .project-header__actions {
        flex-shrink: 0;
    }

    .project-header__description {
        max-width: 20rem;
    }
}
</style>
