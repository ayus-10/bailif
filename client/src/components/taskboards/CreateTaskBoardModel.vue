<script setup>
import { computed, reactive, ref } from "vue";
import ColorInput from "@/components/common/ColorInput.vue";
import { useToast } from "@/composables/useToast";
import { DEFAULT_COLORS } from "@/constants/globals";
import { useTaskboardsStore } from "@/stores/taskboards.store";
import { showApiError } from "@/utils/errorHandlers";

/**
 * @typedef {import("@/types/taskboards").TaskboardForm} TaskboardForm
 * @typedef {import("@/types/taskboards").TaskboardPayload} TaskboardPayload
 */

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
    projectId: {
        type: Number,
        required: true,
    },
});

const emit = defineEmits(["close"]);

/**
 * @type {import("vue").Reactive<TaskboardForm>}
 */
const form = reactive({
    name: "",
    description: "",
    color: DEFAULT_COLORS[0].value,
});

const toast = useToast();

const taskboardsStore = useTaskboardsStore();

const isLoading = computed(
    () => taskboardsStore.taskboardMutationStatus("create") === "loading"
);

const rules = {
    required: (/** @type {string} */ v) =>
        !!v?.trim() || "Taskboard name is required",
};

function close() {
    emit("close");
}

function resetForm() {
    form.name = "";
    form.description = "";
    form.color = DEFAULT_COLORS[0].value;
}

async function submit() {
    if (!form.name.trim()) return;

    /**
     * @type {TaskboardPayload}
     */
    const payload = {
        ...form,
        project_public_id: props.projectId,
    };

    try {
        await taskboardsStore.create(payload);

        resetForm();
        close();
    } catch (err) {
        showApiError(err, toast);
    }
}
</script>

<template>
    <v-dialog
        :model-value="modelValue"
        max-width="32.5rem"
        @update:model-value="close"
    >
        <v-card class="taskboard-dialog" variant="outlined">
            <div class="card-header">
                <h2 class="text-h6 font-weight-bold card-title">
                    Create Taskboard
                </h2>

                <p class="text-caption text-medium-emphasis mb-0 mt-1">
                    Organize project work into a dedicated taskboard.
                </p>
            </div>

            <v-divider />

            <v-card-text class="pa-5">
                <div class="form-group mb-4">
                    <label class="field-label">
                        Taskboard Name
                        <span class="required-mark">*</span>
                    </label>

                    <v-text-field
                        v-model="form.name"
                        placeholder="e.g. Product Development"
                        :rules="[rules.required]"
                        variant="outlined"
                        density="compact"
                        hide-details="auto"
                        autofocus
                        class="custom-field"
                        @keyup.enter="submit"
                    />
                </div>

                <div class="form-group mb-4">
                    <label class="field-label">Description</label>

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

                <div class="appearance-section">
                    <div class="section-label mb-3">Appearance</div>

                    <ColorInput v-model="form.color" />
                </div>
            </v-card-text>

            <v-divider />

            <v-card-actions class="pa-5">
                <v-spacer />

                <v-btn variant="text" class="text-none" @click="close">
                    Cancel
                </v-btn>

                <v-btn
                    color="primary"
                    variant="flat"
                    class="text-none font-weight-medium px-5"
                    @click="submit"
                    :disabled="isLoading"
                    :loading="isLoading"
                >
                    Create Taskboard
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
.taskboard-dialog {
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
