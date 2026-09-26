<script setup>
import { useRouter } from "vue-router";
import { computed } from "vue";
import OnboardingTaskboardForm from "@/components/onboarding/OnboardingTaskboardForm.vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { useTaskboardsStore } from "@/stores/taskboards.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/taskboards").TaskboardForm} TaskboardForm
 */

const { projectId } = useActiveProject();

const taskboardsStore = useTaskboardsStore();
const router = useRouter();
const toast = useToast();

const isLoading = computed(
    () => taskboardsStore.taskboardMutationStatus("create") === "loading"
);

/**
 * @param {TaskboardForm} form
 */
async function handleCreateTaskboard(form) {
    if (!projectId.value) return;
    if (isLoading.value) return;

    try {
        /**
         * @type {import("@/types/taskboards").TaskboardPayload}
         */
        const payload = {
            ...form,
            project_public_id: projectId.value,
        };

        await taskboardsStore.create(payload);

        router.push({ name: "dashboard" });
    } catch (err) {
        showApiError(err, toast);
    }
}
</script>

<template>
    <div class="new-taskboard-wrapper">
        <OnboardingTaskboardForm
            v-if="projectId"
            :is-loading="isLoading"
            @submit="handleCreateTaskboard"
        />

        <NoActiveProject v-else />
    </div>
</template>

<style scoped>
.new-taskboard-wrapper {
    min-height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    background-color: #f4f5f7;
}
</style>
