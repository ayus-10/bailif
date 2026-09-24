<script setup>
import { onMounted, reactive, ref } from "vue";
import ColorInput from "@/components/common/ColorInput.vue";
import IconInput from "@/components/common/IconInput.vue";
import { DEFAULT_COLORS, DEFAULT_ICONS } from "@/constants/globals";

/**
 * @typedef {import("@/stores/projects.store").ProjectCreate} ProjectCreate
 * @typedef {import("vue").Ref<InstanceType<typeof import("vuetify/components").VForm> | null>} VFormRef
 * @typedef {ProjectCreate & { color?: string }} ProjectCreateForm
 */

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits({
    submit: (form) => !!form,
});

/**
 * @type {VFormRef}
 */
const formRef = ref(null);

/**
 * @type {import("vue").Reactive<ProjectCreateForm>}
 */
const form = reactive({
    name: "",
    description: "",
    icon: DEFAULT_ICONS[0].value,
    color: DEFAULT_COLORS[0].value,
    agent_enabled: false,
    status: "active",
    start_date: null,
    target_end_date: null,
    actual_end_date: null,
    timezone: null,
});

const rules = {
    required: (/** @type {string} */ v) =>
        !!v?.trim() || "Project name is required",
};

onMounted(() => {
    form.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
});

async function handleSubmit() {
    if (!formRef.value || props.isLoading) return;

    const { valid } = await formRef.value.validate();

    if (!valid) return;

    emit("submit", { ...form });
}
</script>

<template>
    <div class="new-project-wrapper">
        <v-card class="new-project-card" variant="outlined">
            <div class="card-header">
                <h1 class="text-h6 font-weight-bold card-title">
                    Create New Project
                </h1>
                <p class="text-caption text-medium-emphasis mb-0 mt-1">
                    Set up basic details and assistant capabilities for your
                    workspace.
                </p>
            </div>

            <v-divider />

            <v-card-text class="pa-5">
                <v-form ref="formRef" @submit.prevent="handleSubmit">
                    <div class="form-section">
                        <div class="form-group mb-4">
                            <label class="field-label">
                                Project Name
                                <span class="required-mark">*</span>
                            </label>

                            <v-text-field
                                v-model="form.name"
                                placeholder="e.g. System Architecture"
                                :rules="[rules.required]"
                                variant="outlined"
                                density="compact"
                                hide-details="auto"
                                autofocus
                                class="custom-field"
                            />
                        </div>

                        <div class="form-group mb-4">
                            <label class="field-label">Description</label>

                            <v-textarea
                                v-model="form.description"
                                placeholder="Brief summary of project scope"
                                variant="outlined"
                                density="compact"
                                rows="2"
                                no-resize
                                hide-details
                                auto-grow
                                class="custom-field"
                            />
                        </div>

                        <div class="appearance-section mb-5">
                            <div class="section-label mb-3">Appearance</div>

                            <div class="appearance-controls">
                                <IconInput v-model="form.icon" />
                                <ColorInput v-model="form.color" />
                            </div>
                        </div>
                    </div>

                    <div class="settings-box mb-5">
                        <div class="d-flex align-center justify-space-between">
                            <div>
                                <div
                                    class="text-subtitle-2 font-weight-semibold"
                                >
                                    Enable Agent
                                </div>

                                <div class="text-caption text-medium-emphasis">
                                    Allow automated task actions for this
                                    project
                                </div>
                            </div>

                            <v-switch
                                v-model="form.agent_enabled"
                                color="primary"
                                density="compact"
                                hide-details
                                inset
                            />
                        </div>
                    </div>

                    <div class="d-flex align-center justify-end gap-3 mt-4">
                        <v-btn
                            type="submit"
                            color="primary"
                            variant="flat"
                            density="comfortable"
                            class="text-none font-weight-medium px-5"
                            :loading="props.isLoading"
                            :disabled="props.isLoading"
                        >
                            Next Step
                        </v-btn>
                    </div>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<style scoped>
.new-project-wrapper {
    min-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    background-color: #f4f5f7;
}

.new-project-card {
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

.settings-box {
    padding: 0.875rem 1rem;
    background-color: rgb(var(--v-theme-surface-container, 248, 249, 250));
    border: 1px solid rgb(var(--v-theme-outline-container, 234, 236, 240));
    border-radius: 0.375rem;
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
