<script setup>
import { useRouter } from "vue-router";
import { computed, ref } from "vue";
import ConfirmDialog from "@/components/common/ConfirmDialog.vue";
import ProjectForm from "@/components/projects/ProjectForm.vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import {
    useDeleteProject,
    useProject,
    useUpdateProject,
} from "@/queries/projects.queries";
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

const { projectId: activeProjectId } = useActiveProject();

const projectId = computed(() => Number(props.id));

const projectQuery = useProject(projectId, { refetchOnMount: "always" });
const project = computed(() => projectQuery.data.value ?? null);
const hasLoadError = computed(
    () => projectQuery.isError.value && !project.value
);
const hasRefreshError = computed(
    () => projectQuery.isError.value && !!project.value
);
const updateMutation = useUpdateProject();
const deleteMutation = useDeleteProject();

const isActive = computed(() => activeProjectId.value === projectId.value);

const isSaving = computed(() => updateMutation.isPending.value);

const isDeleting = computed(() => deleteMutation.isPending.value);

const showDeleteDialog = ref(false);

function load() {
    projectQuery.refetch();
}

/**
 * @param {ProjectUpdate} payload
 */
async function handleSubmit(payload) {
    if (isSaving.value) return;

    try {
        await updateMutation.mutateAsync({ id: projectId.value, payload });

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
        await deleteMutation.mutateAsync(projectId.value);

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
        <v-skeleton-loader
            v-if="!project && projectQuery.isLoading.value"
            type="article, article"
        />

        <div v-else-if="hasLoadError" class="project-settings__message">
            <v-icon icon="mdi-alert-circle-outline" size="32" />

            <p>We couldn't load this project's settings.</p>

            <div class="d-flex ga-2">
                <v-btn
                    color="primary"
                    variant="flat"
                    class="text-none"
                    @click="load"
                >
                    Try again
                </v-btn>

                <v-btn variant="text" class="text-none" @click="handleCancel">
                    Back
                </v-btn>
            </div>
        </div>

        <template v-else-if="project">
            <v-alert
                v-if="hasRefreshError"
                type="error"
                variant="tonal"
                class="project-settings__load-error"
            >
                <div class="d-flex align-center justify-space-between ga-2">
                    <span>We couldn't refresh this project's settings.</span>
                    <div class="d-flex ga-2">
                        <v-btn size="small" @click="load">Retry</v-btn>
                        <v-btn
                            size="small"
                            variant="text"
                            @click="handleCancel"
                        >
                            Back
                        </v-btn>
                    </div>
                </div>
            </v-alert>

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

.project-settings__message {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 2rem 1rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
}

.project-settings__load-error {
    max-width: 35rem;
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
