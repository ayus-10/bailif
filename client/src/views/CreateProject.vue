<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
import ProjectForm from "@/components/projects/ProjectForm.vue";
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

        await router.push(`/dashboard/project/${projectId}`);
    } catch (err) {
        showApiError(err, toast);
    }
}

function handleCancel() {
    router.back();
}
</script>

<template>
    <main class="project-page">
        <ProjectForm
            :loading="isLoading"
            @submit="handleSubmit"
            @cancel="handleCancel"
        />
    </main>
</template>

<style scoped>
.project-page {
    width: 100%;
    max-width: 40rem;
    margin: 0 auto;
    padding: 2rem 1rem 3rem;
}
</style>
