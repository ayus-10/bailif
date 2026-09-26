<script setup>
import { useRouter } from "vue-router";
import { onMounted } from "vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import ProjectCard from "@/components/projects/ProjectCard.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useProjectsStore } from "@/stores/projects.store";

const projectsStore = useProjectsStore();

const { projectId: activeProjectId } = useActiveProject();

const router = useRouter();

onMounted(() => {
    projectsStore.fetch();
});

function retry() {
    projectsStore.fetch({ forceRefresh: true });
}

function switchProject() {}

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

        <div v-if="activeProjectId" class="project-page__grid">
            <ProjectCard
                v-for="project in projectsStore.items"
                :key="project.public_id"
                :project="project"
                :active-project-id="activeProjectId"
                @switch="switchProject"
            />
        </div>

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
