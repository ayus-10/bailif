<script setup>
import { computed, ref } from "vue";
import { formatDate } from "@/utils/dateFormatters";

/**
 * @typedef {import("@/types/project").ProjectRead} ProjectRead
 */

const props = defineProps({
    project: {
        /**
         * @type {import("vue").PropType<ProjectRead>}
         */
        type: Object,
        required: true,
    },
    activeProjectId: {
        type: Number,
        default: null,
    },
});

const emit = defineEmits(["switch", "rename", "duplicate", "delete"]);

const isActive = computed(
    () => props.project.public_id === props.activeProjectId
);

const overviewRoute = computed(() => ({
    name: "project-overview",
    params: {
        id: props.project.public_id,
    },
}));

const formattedUpdatedDate = computed(() => {
    if (!props.project.updated_at) {
        return "";
    }

    return formatDate(props.project.updated_at);
});

const formattedStartDate = computed(() => {
    if (!props.project.start_date) {
        return "";
    }

    return formatDate(props.project.start_date);
});

function handleClick() {
    if (isActive.value) {
        return;
    }

    emit("switch", props.project);
}

/**
 * @type {import("vue").Ref<[number, number] | HTMLElement>}
 */
const contextMenuTarget = ref([0, 0]);
const contextMenuOpen = ref(false);

/**
 * @param {MouseEvent} event
 */
function openContextMenuAtCursor(event) {
    event.preventDefault();
    contextMenuTarget.value = [event.clientX, event.clientY];
    contextMenuOpen.value = true;
}

/**
 * @param {MouseEvent} event
 */
function openContextMenuFromButton(event) {
    event.preventDefault();
    event.stopPropagation();
    contextMenuTarget.value = /** @type {HTMLElement} */ (event.currentTarget);
    contextMenuOpen.value = true;
}

function handleSetActive() {
    contextMenuOpen.value = false;
    handleClick();
}

function handleRename() {
    contextMenuOpen.value = false;
    emit("rename", props.project);
}

function handleDuplicate() {
    contextMenuOpen.value = false;
    emit("duplicate", props.project);
}

function handleDelete() {
    contextMenuOpen.value = false;
    emit("delete", props.project);
}
</script>

<template>
    <v-card
        :to="overviewRoute"
        variant="outlined"
        rounded="lg"
        class="project-card"
        :class="{ 'project-card--active': isActive }"
        v-ripple
        :aria-label="
            isActive
                ? `${project.name}, currently active project`
                : `Switch to ${project.name}`
        "
        :aria-current="isActive ? 'page' : undefined"
        @click="handleClick"
        @contextmenu="openContextMenuAtCursor"
    >
        <div class="project-card__header">
            <div class="project-card__identity">
                <div class="project-card__icon" aria-hidden="true">
                    <v-icon
                        :icon="project.icon || 'mdi-folder-outline'"
                        size="18"
                    />
                </div>

                <h3 class="project-card__title">
                    {{ project.name }}
                </h3>
            </div>

            <div class="project-card__actions">
                <span v-if="isActive" class="project-card__active-badge">
                    Active
                </span>

                <button
                    type="button"
                    class="project-card__icon-btn"
                    v-ripple
                    aria-label="Project actions"
                    @click="openContextMenuFromButton"
                >
                    <v-icon icon="mdi-dots-horizontal" size="14" />
                </button>
            </div>
        </div>

        <p v-if="project.description" class="project-card__description">
            {{ project.description }}
        </p>

        <div
            v-if="formattedStartDate || project.target_end_date"
            class="project-card__dates"
        >
            <span v-if="formattedStartDate">
                Started {{ formattedStartDate }}
            </span>

            <span
                v-if="formattedStartDate && project.target_end_date"
                class="project-card__meta-separator"
                aria-hidden="true"
            />

            <span v-if="project.target_end_date">
                Due {{ formatDate(project.target_end_date) }}
            </span>

            <span
                v-if="formattedUpdatedDate"
                class="project-card__meta-separator"
                aria-hidden="true"
            />

            <span v-if="formattedUpdatedDate">
                Updated {{ formattedUpdatedDate }}
            </span>
        </div>
    </v-card>

    <v-menu
        v-model="contextMenuOpen"
        :target="contextMenuTarget"
        density="compact"
    >
        <v-list density="compact">
            <v-list-item
                v-if="!isActive"
                title="Set as active"
                @click="handleSetActive"
            >
                <template #prepend>
                    <v-icon icon="mdi-check-circle-outline" size="1.125rem" />
                </template>
            </v-list-item>

            <v-list-item title="Rename" @click="handleRename">
                <template #prepend>
                    <v-icon icon="mdi-pencil-outline" size="1.125rem" />
                </template>
            </v-list-item>

            <v-list-item title="Duplicate" @click="handleDuplicate">
                <template #prepend>
                    <v-icon icon="mdi-content-copy" size="1.125rem" />
                </template>
            </v-list-item>

            <v-divider />

            <v-list-item
                title="Delete"
                base-color="error"
                @click="handleDelete"
            >
                <template #prepend>
                    <v-icon icon="mdi-delete-outline" size="1.125rem" />
                </template>
            </v-list-item>
        </v-list>
    </v-menu>
</template>

<style scoped>
.project-card {
    --project-accent: rgb(var(--v-theme-primary));

    position: relative;
    display: block;
    width: 100%;
    min-height: 9.25rem;
    padding: 1rem;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
    box-shadow: none;
    text-decoration: none;
    transition:
        border-color 0.12s ease,
        background-color 0.12s ease;
}

.project-card:hover {
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

.project-card:focus {
    outline: none;
}

.project-card:focus-visible {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

.project-card__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
    min-width: 0;
}

.project-card__identity {
    display: flex;
    align-items: center;
    min-width: 0;
    gap: 0.625rem;
}

.project-card__icon {
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

.project-card__title {
    min-width: 0;
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.project-card__actions {
    display: flex;
    align-items: center;
    flex: 0 0 auto;
    gap: 0.5rem;
}

.project-card__active-badge {
    flex: 0 0 auto;
    padding: 0.1875rem 0.5rem;
    border-radius: 0.125rem;
    background: rgba(var(--v-theme-primary), 0.08);
    color: rgb(var(--v-theme-primary));
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.project-card__icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    width: 1.5rem;
    height: 1.5rem;
    padding: 0;
    border: none;
    border-radius: 0.375rem;
    background: transparent;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    cursor: pointer;
    transition:
        background-color 0.12s ease,
        color 0.12s ease;
}

.project-card__icon-btn:hover {
    background: rgb(var(--v-theme-surface));
    color: rgb(var(--v-theme-on-surface));
}

.project-card__icon-btn:focus-visible {
    outline: none;
    box-shadow: 0 0 0 0.125rem rgba(var(--v-theme-primary), 0.15);
}

.project-card__description {
    margin: 0.625rem 0 0;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    line-height: 1.25rem;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
}

.project-card__meta,
.project-card__dates {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
    line-height: 1rem;
}

.project-card__meta {
    margin-top: 0.875rem;
}

.project-card__dates {
    margin-top: 0.375rem;
}

.project-card__meta-separator {
    width: 0.1875rem;
    height: 0.1875rem;
    flex: 0 0 auto;
    border-radius: 50%;
    background: rgb(var(--v-theme-text-disabled, 148, 157, 173));
}
</style>
