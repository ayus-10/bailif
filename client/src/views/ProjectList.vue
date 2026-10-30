<script setup>
import { useRouter } from "vue-router";
import { computed, onMounted } from "vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import ProjectCard from "@/components/projects/ProjectCard.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { useAuthStore } from "@/stores/auth";
import { useProjectsStore } from "@/stores/projects.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/project").ProjectRead} ProjectRead
 */

const authStore = useAuthStore();
const projectsStore = useProjectsStore();
const toast = useToast();

const { projectId: activeProjectId } = useActiveProject();

const router = useRouter();

const status = computed(() => projectsStore.fetchListStatus());
const isLoadingFirstPage = computed(
    () => status.value === "loading" && projectsStore.items.length === 0
);
const hasError = computed(
    () => status.value === "error" && projectsStore.items.length === 0
);

onMounted(load);

function load() {
    projectsStore
        .fetch({ forceRefresh: true })
        .catch((err) => showApiError(err, toast));
}

function loadMore() {
    projectsStore.loadMore().catch((err) => showApiError(err, toast));
}

/**
 * @param {ProjectRead} project
 */
async function switchProject(project) {
    try {
        await authStore.setActiveProject(project.public_id);
        toast.success(`${project.name} is now your active project`);
    } catch (err) {
        showApiError(err, toast);
    }
}

/**
 * @param {string} action
 */
function handleNavigate(action) {
    router.push({ name: action });
}
</script>

<template>
    <v-container fluid class="project-page">
        <ProjectHeader
            title="Projects"
            show-new-project
            @new-project="handleNavigate('project-new')"
            @navigate="handleNavigate"
        />

        <v-skeleton-loader
            v-if="isLoadingFirstPage"
            type="article, article"
            class="project-page__skeleton"
        />

        <div v-else-if="hasError" class="project-page__message">
            <v-icon icon="mdi-alert-circle-outline" size="32" />

            <p>We couldn't load your projects.</p>

            <v-btn
                color="primary"
                variant="flat"
                class="text-none"
                @click="load"
            >
                Try again
            </v-btn>
        </div>

        <template v-else-if="activeProjectId">
            <div class="project-page__grid">
                <ProjectCard
                    v-for="project in projectsStore.items"
                    :key="project.public_id"
                    :project="project"
                    :active-project-id="activeProjectId"
                    @switch="switchProject"
                />
            </div>

            <div v-if="projectsStore.nextCursor" class="project-page__more">
                <v-btn
                    variant="tonal"
                    color="primary"
                    class="text-none"
                    :loading="status === 'loading'"
                    @click="loadMore"
                >
                    Load more
                </v-btn>
            </div>
        </template>

        <NoActiveProject v-else class="project-page__empty" />
    </v-container>
</template>

<style scoped>
.project-page {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    padding: 1.5rem;
}

.project-page__grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 0.75rem 0;
    width: 100%;
}

.project-page__message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 3rem 1rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}

.project-page__more {
    display: flex;
    justify-content: center;
    padding: 0.5rem 0 1rem;
}

.project-page__empty {
    flex: 1;
    min-height: 0;
}

@media (min-width: 960px) {
    .project-page__grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (min-width: 1280px) {
    .project-page__grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
}
</style>
