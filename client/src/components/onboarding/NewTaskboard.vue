<script setup>
import { useRouter } from "vue-router";
import { computed, reactive, ref } from "vue";
import ColorInput from "@/components/common/ColorInput.vue";
import NoActiveProject from "@/components/projects/NoActiveProject.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { DEFAULT_COLORS } from "@/constants/globals";
import { useTaskboardsStore } from "@/stores/taskboards.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("vue").Ref<InstanceType<typeof import("vuetify/components").VForm> | null>} VFormRef
 * @typedef {import("@/types/taskboards").TaskboardForm} TaskboardForm
 * @typedef {import("@/types/taskboards").TaskboardPayload} TaskboardPayload
 */

const { projectId } = useActiveProject();

const toast = useToast();

/**
 * @type {VFormRef}
 */
const formRef = ref(null);

const taskboardsStore = useTaskboardsStore();

const router = useRouter();

const isLoading = computed(
    () => taskboardsStore.taskboardMutationStatus("create") === "loading"
);

/**
 * @type {import("vue").Reactive<TaskboardForm>}
 */
const form = reactive({
    name: "",
    description: "",
    color: DEFAULT_COLORS[0].value,
});

const rules = {
    required: (/** @type {string} */ v) =>
        !!v?.trim() || "Taskboard name is required",
};

async function handleSubmit() {
    if (!projectId.value) return;
    if (!formRef.value) return;

    const { valid } = await formRef.value.validate();
    if (!valid) return;

    try {
        /**
         * @type {TaskboardPayload}
         */
        const payload = {
            ...form,
            project_public_id: projectId.value,
        };

        await taskboardsStore.create(payload);

        router.push("/dashboard");
    } catch (err) {
        showApiError(err, toast);
    }
}
</script>

<template>
    <div class="new-taskboard-wrapper">
        <v-card v-if="projectId" class="new-taskboard-card" variant="outlined">
            <div class="card-header">
                <h1 class="text-h6 font-weight-bold card-title">
                    Create New Taskboard
                </h1>

                <p class="text-caption text-medium-emphasis mb-0 mt-1">
                    Organize your project work into a dedicated taskboard.
                </p>
            </div>

            <v-divider />

            <v-card-text class="pa-5">
                <v-form ref="formRef" @submit.prevent="handleSubmit">
                    <div class="form-section">
                        <div class="form-group mb-4">
                            <label class="field-label">
                                Taskboard Name
                                <span class="required-mark">*</span>
                            </label>

                            <v-text-field
                                v-model="form.name"
                                placeholder="e.g. Sprint Planning"
                                :rules="[rules.required]"
                                variant="outlined"
                                density="compact"
                                hide-details="auto"
                                autofocus
                                class="custom-field"
                            />
                        </div>

                        <div class="form-group mb-4">
                            <label class="field-label"> Description </label>

                            <v-textarea
                                v-model="form.description"
                                placeholder="Brief summary of what this taskboard is for"
                                variant="outlined"
                                density="compact"
                                rows="2"
                                no-resize
                                hide-details
                                class="custom-field"
                            />
                        </div>

                        <div class="appearance-section mb-5">
                            <div class="section-label mb-3">Appearance</div>

                            <div class="appearance-controls">
                                <ColorInput v-model="form.color" />
                            </div>
                        </div>
                    </div>

                    <div class="d-flex align-center justify-end gap-3 mt-4">
                        <v-btn
                            type="submit"
                            color="primary"
                            variant="flat"
                            density="comfortable"
                            class="text-none font-weight-medium px-5"
                            :loading="isLoading"
                            :disabled="isLoading"
                        >
                            Create Taskboard
                        </v-btn>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>

        <NoActiveProject v-else />
    </div>
</template>

<style scoped>
.new-taskboard-wrapper {
    min-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    background-color: #f4f5f7;
}

.new-taskboard-card {
    width: 100%;
    max-width: 32.5rem;
    background-color: #fff;
    border: 1px solid rgb(var(--v-theme-outline, 225, 228, 232));
    border-radius: 0.5rem;
    box-shadow: none;
}

.card-header {
    padding: 1.25rem 1.25rem 1rem;
}

.card-title {
    color: rgb(var(--v-theme-on-surface));
    line-height: 1.2;
    letter-spacing: -0.01em;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.field-label {
    margin-bottom: 0.375rem;
    font-size: 0.8125rem;
    font-weight: 600;
    color: #344054;
}

.required-mark {
    color: #d92d20;
}

.appearance-section {
    display: flex;
    flex-direction: column;
}

.section-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #344054;
}

.appearance-controls {
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
}

:deep(.v-field) {
    background-color: #fff;
    border-radius: 0.375rem;
}

:deep(.v-field--outlined .v-field__outline) {
    --v-field-border-opacity: 1;
    color: #d0d5dd;
}

:deep(.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
}

:deep(.v-btn) {
    border-radius: 0.375rem;
    box-shadow: none;
}
</style>
