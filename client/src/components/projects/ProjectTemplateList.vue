<script setup>
import { computed, onMounted } from "vue";
import PreviewProjectCard from "@/components/projects/PreviewProjectCard.vue";
import { useProjectsStore } from "@/stores/projects.store";

/**
 * @typedef {import("@/types/project").ProjectRead} ProjectTemplate
 */

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: true,
    },
    title: {
        type: String,
        default: "Duplicate from an existing project",
    },
    limit: {
        type: Number,
        default: 6,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue", "select"]);

const projectsStore = useProjectsStore();

onMounted(() => {
    projectsStore.fetch();
});

const templates = computed(() => {
    const cached = projectsStore.items ?? [];
    return cached
        .sort(
            (a, b) =>
                new Date(b.updated_at).getTime() -
                new Date(a.updated_at).getTime()
        )
        .slice(0, props.limit);
});

const hasTemplates = computed(() => templates.value.length > 0);

function toggle() {
    emit("update:modelValue", !props.modelValue);
}

/**
 * @param {ProjectTemplate} project
 */
function selectTemplate(project) {
    if (props.disabled) return;
    emit("select", project);
}
</script>

<template>
    <section
        class="project-template-panel"
        :class="{ 'project-template-panel--collapsed': !modelValue }"
        :aria-label="title"
    >
        <header class="project-template-panel__header">
            <h3 class="project-template-panel__title">{{ title }}</h3>

            <v-btn
                icon
                variant="text"
                size="small"
                class="project-template-panel__toggle"
                :aria-expanded="modelValue"
                :aria-label="modelValue ? `Hide ${title}` : `Show ${title}`"
                @click="toggle"
            >
                <v-icon
                    :icon="
                        modelValue ? 'mdi-chevron-right' : 'mdi-chevron-left'
                    "
                />
            </v-btn>
        </header>

        <transition name="project-template-panel-swoop">
            <div v-if="modelValue" class="project-template-panel__body">
                <div class="project-template-panel__list">
                    <PreviewProjectCard
                        v-for="project in templates"
                        :key="project.public_id"
                        :project="project"
                        :disabled="disabled"
                        @select="selectTemplate(project)"
                    />

                    <p
                        v-if="!hasTemplates"
                        class="project-template-panel__empty-title"
                    >
                        No projects to duplicate from yet
                    </p>
                </div>
            </div>
        </transition>
    </section>
</template>

<style scoped>
.project-template-panel {
    height: 100%;
    display: flex;
    flex-direction: column;
    width: 100%;
    border: 0.0625rem solid rgb(var(--v-theme-outline, 225, 228, 232));
    border-radius: 0.75rem;
    background-color: rgb(var(--v-theme-surface, 255, 255, 255));
    overflow: hidden;
}

.project-template-panel__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 0.0625rem solid rgb(var(--v-theme-outline, 225, 228, 232));
    background-color: rgb(var(--v-theme-surface, 255, 255, 255));
}

.project-template-panel--collapsed .project-template-panel__header {
    border-bottom: none;
}

.project-template-panel__title {
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: rgb(var(--v-theme-on-surface, 26, 31, 44));
    margin: 0;
}

.project-template-panel__toggle {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    border-radius: 0.5rem;
}

.project-template-panel__body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 0.625rem;
    background-color: rgb(var(--v-theme-surface, 255, 255, 255));
}

.project-template-panel__list {
    display: flex;
    flex-direction: column;
}

.project-template-panel__empty-title {
    min-height: 2.25rem;
    display: flex;
    align-items: center;
    font-size: 0.8125rem;
    font-weight: 500;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    margin: 0;
}

.project-template-panel-swoop-enter-active,
.project-template-panel-swoop-leave-active {
    transition:
        transform 0.2s ease,
        opacity 0.2s ease;
}

.project-template-panel-swoop-enter-from,
.project-template-panel-swoop-leave-to {
    transform: translateX(100%);
    opacity: 0;
}
</style>
