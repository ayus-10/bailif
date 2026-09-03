<script setup>
import { reactive } from "vue";
import ColorInput from "@/components/common/ColorInput.vue";
import { DEFAULT_COLORS } from "@/constants/globals";

/** @typedef {import('@/types/taskboard').TaskboardForm} TaskboardForm */

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },

    projectId: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["close", "submit"]);

/** @type {import("vue").Reactive<TaskboardForm>} */
const form = reactive({
    name: "",
    description: "",
    color: DEFAULT_COLORS[0].value,
    project_id: props.projectId,
});

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
    form.project_id = props.projectId;
}

async function submit() {
    if (!form.name.trim()) return;

    emit("submit", {
        name: form.name.trim(),
        description: form.description.trim() || null,
        color: form.color,
        project_id: form.project_id,
    });

    resetForm();
    close();
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
    border: 1px solid #e1e4e8;
    border-radius: 0.5rem;
    box-shadow: none;
}

.card-header {
    padding: 1.25rem 1.25rem 1rem;
}

.card-title {
    color: #1a1f2c;
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
