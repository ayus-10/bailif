<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
import ProjectForm from "@/components/projects/ProjectForm.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import ProjectTemplateList from "@/components/projects/ProjectTemplateList.vue";
import { useToast } from "@/composables/useToast";
import { useProjectsStore } from "@/stores/projects.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/project").ProjectCreate} ProjectCreate
 */

const router = useRouter();
const toast = useToast();
const projectsStore = useProjectsStore();

const isLoading = computed(
    () => projectsStore.projectMutationStatus("create") === "loading"
);

/**
 * @param {ProjectCreate} project
 */
async function handleSubmit(project) {
    if (isLoading.value) return;

    try {
        const createdProject = await projectsStore.create(project);

        const projectId = createdProject.public_id;

        router.push({
            name: "project-overview",
            params: { id: projectId },
        });
    } catch (err) {
        showApiError(err, toast);
    }
}

function handleCancel() {
    router.back();
}
</script>

<template>
    <div class="create-project-page">
        <ProjectHeader
            description="Create a new project to manage your workspace"
        />
        <main class="project-page">
            <div class="project-page__form">
                <ProjectForm
                    :loading="isLoading"
                    @submit="handleSubmit"
                    @cancel="handleCancel"
                />
            </div>

            <aside class="project-page__templates">
                <ProjectTemplateList />
            </aside>
        </main>
    </div>
</template>

<style scoped>
.create-project-page {
    display: flex;
    flex-direction: column;
    height: 100dvh;
    padding: 2rem 1.5rem;
    overflow: hidden;
}

.project-page {
    width: 100%;
    margin: 0 auto;
    padding: 1rem 0;
    display: flex;
    justify-content: space-between;
    gap: 1.5rem;
    flex: 1;
    min-height: 0;
}

.project-page__form,
.project-page__templates {
    min-width: 0;
    min-height: 0;
    height: 100%;
}

.project-page__form {
    flex: 1 1 50%;
    overflow-y: auto;
}

.project-page__templates {
    flex: 0 0 auto;
    max-width: 26rem;
}

@media (max-width: 960px) {
    .create-project-page {
        height: auto;
        overflow: visible;
        padding: 1.5rem 1rem;
    }

    .project-page {
        flex-direction: column;
        flex: initial;
        min-height: auto;
        gap: 1rem;
    }

    .project-page__form,
    .project-page__templates {
        height: auto;
        max-width: none;
        overflow: visible;
    }
}
</style>
