<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
import OnboardingProjectForm from "@/components/onboarding/OnboardingProjectForm.vue";
import { useToast } from "@/composables/useToast";
import { useAuthStore } from "@/stores/auth";
import { useProjectsStore } from "@/stores/projects.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/stores/projects.store").ProjectCreate} ProjectCreate
 * @typedef {ProjectCreate & { color?: string }} ProjectCreateForm
 */

const authStore = useAuthStore();
const projectsStore = useProjectsStore();
const router = useRouter();
const toast = useToast();

const isLoading = computed(
    () => projectsStore.projectMutationStatus("create") === "loading"
);

/**
 * @param {ProjectCreateForm} project
 */
async function handleCreateProject(project) {
    if (isLoading.value) return;

    try {
        await projectsStore.create(project);

        authStore.refreshCurrentUser();

        router.push({ name: "taskboard" });
    } catch (err) {
        showApiError(err, toast);
    }
}
</script>

<template>
    <div class="new-project-wrapper">
        <OnboardingProjectForm
            :is-loading="isLoading"
            @submit="handleCreateProject"
        />
    </div>
</template>

<style scoped>
.new-project-wrapper {
    min-height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    background-color: #f4f5f7;
}
</style>
