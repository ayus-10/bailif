<script setup>
import { useRouter } from "vue-router";
import { computed, ref, watch } from "vue";
import ConfirmDialog from "@/components/common/ConfirmDialog.vue";
import ProjectForm from "@/components/projects/ProjectForm.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { useProjectsStore } from "@/stores/projects.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/project").ProjectUpdate} ProjectUpdate
 */

const props = defineProps({
    id: {
        type: String,
        required: true,
    },
});

const router = useRouter();
const toast = useToast();
const projectsStore = useProjectsStore();

const { projectId: activeProjectId } = useActiveProject();

const projectId = computed(() => Number(props.id));

const project = computed(() =>
    projectsStore.currentProject?.public_id === projectId.value
        ? projectsStore.currentProject
        : null
);

const isActive = computed(() => activeProjectId.value === projectId.value);

const isSaving = computed(
    () =>
        projectsStore.projectMutationStatus("update", projectId.value) ===
        "loading"
);

const isDeleting = computed(
    () =>
        projectsStore.projectMutationStatus("delete", projectId.value) ===
        "loading"
);

const showDeleteDialog = ref(false);

watch(projectId, load, { immediate: true });

function load() {
    projectsStore
        .get(projectId.value)
        .catch((err) => showApiError(err, toast));
}

/**
 * @param {ProjectUpdate} payload
 */
async function handleSubmit(payload) {
    if (isSaving.value) return;

    try {
        await projectsStore.update(projectId.value, payload);

        toast.success("Project updated");
        router.push({
            name: "project-overview",
            params: { id: projectId.value },
        });
    } catch (err) {
        showApiError(err, toast);
    }
}

async function handleDelete() {
    try {
        await projectsStore.remove(projectId.value);

        showDeleteDialog.value = false;
        router.push({ name: "project-list" });
    } catch (err) {
        showApiError(err, toast);
    }
}

function handleCancel() {
    router.back();
}
</script>

<template>
    <v-container fluid class="project-settings">
        <v-skeleton-loader v-if="!project" type="article, article" />

        <template v-else>
            <ProjectHeader title="Project settings" :project="project" />

            <div class="project-settings__form">
                <ProjectForm
                    :key="project.public_id"
                    :initial-values="project"
                    submit-label="Save changes"
                    :loading="isSaving"
                    @submit="handleSubmit"
                    @cancel="handleCancel"
                />
            </div>

            <section class="project-settings__danger">
                <div>
                    <h3 class="project-settings__danger-title">
                        Delete project
                    </h3>

                    <p class="project-settings__danger-text">
                        {{
                            isActive
                                ? "The active project can't be deleted. Switch to another project first."
                                : "Deletes the project along with its tasks and taskboards."
                        }}
                    </p>
                </div>

                <v-btn
                    color="error"
                    variant="outlined"
                    class="text-none"
                    :disabled="isActive"
                    @click="showDeleteDialog = true"
                >
                    Delete project
                </v-btn>
            </section>

            <ConfirmDialog
                v-model="showDeleteDialog"
                title="Delete project"
                :message="`Delete ${project.name}? This also removes all of its tasks and taskboards.`"
                :loading="isDeleting"
                @confirm="handleDelete"
            />
        </template>
    </v-container>
</template>

<style scoped>
.project-settings {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
}

.project-settings__form {
    padding: 0.5rem 0;
}

.project-settings__danger {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    max-width: 35rem;
    padding: 1rem;
    border: 0.0625rem solid rgba(var(--v-theme-error), 0.3);
    border-radius: 0.75rem;
}

.project-settings__danger-title {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 700;
}

.project-settings__danger-text {
    margin: 0.25rem 0 0;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}
</style>
