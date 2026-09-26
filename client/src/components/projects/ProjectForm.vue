<script setup>
import { computed, reactive, ref, watch } from "vue";
import ColorInput from "@/components/common/ColorInput.vue";
import IconInput from "@/components/common/IconInput.vue";
import {
    PERMISSION_ITEMS,
    STATUS_ITEMS,
    TIMEZONE_ITEMS,
} from "@/constants/projects";
import { isoToLocalInput, localInputToIso } from "@/utils/dateFormatters";

/**
 * @typedef {import("@/types/project").ProjectCreate} ProjectCreate
 */

/**
 * @typedef {import("vuetify/components").VForm} VForm
 * @typedef {import("vuetify/components").VTextField} VTextField
 */

const props = defineProps({
    initialValues: { type: Object, default: () => ({}) },
    submitLabel: { type: String, default: "Create project" },
    loading: { type: Boolean, default: false },
});

const emit = defineEmits(["submit", "cancel"]);

const browserTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

const initialFormData = {
    name: props.initialValues.name ?? "",
    description: props.initialValues.description ?? "",
    icon: props.initialValues.icon ?? "",
    color: props.initialValues.color ?? null,
    status: props.initialValues.status ?? "active",
    start_date: isoToLocalInput(props.initialValues.start_date),
    target_end_date: isoToLocalInput(props.initialValues.target_end_date),
    actual_end_date: isoToLocalInput(props.initialValues.actual_end_date),
    timezone: props.initialValues.timezone ?? browserTimezone,
    agent_enabled: props.initialValues.agent_enabled ?? false,
    default_agent_permission_level:
        props.initialValues.default_agent_permission_level ?? "propose_only",
};

const form = reactive(initialFormData);

/**
 * @type {import("vue").Ref<VForm | null>}
 */
const formRef = ref(null);

/**
 * @type {import("vue").Ref<VTextField | null>}
 */
const targetEndRef = ref(null);

/**
 * @type {import("vue").Ref<VTextField | null>}
 */
const actualEndRef = ref(null);

const showActualEnd = computed(
    () => form.status === "completed" || form.status === "archived"
);

const nameRules = [
    (/** @type {string} */ v) => !!v?.trim() || "Name is required",
];

/**
 * @param {string} label
 * @returns {(v: string | null | undefined) => true | string}
 */
const notBeforeStart = (label) => (v) =>
    !v ||
    !form.start_date ||
    v >= form.start_date ||
    `${label} can't be before the start date`;

const targetEndRules = [notBeforeStart("Target end")];
const actualEndRules = [notBeforeStart("Actual end")];

watch(
    () => form.start_date,
    () => {
        targetEndRef.value?.validate();
        actualEndRef.value?.validate();
    }
);

async function onSubmit() {
    if (!formRef.value) return;
    if (props.loading) return;

    const { valid } = await formRef.value.validate();
    if (!valid) return;

    /**
     * @type {ProjectCreate}
     */
    const payload = {
        name: form.name.trim(),
        description: form.description.trim(),
        icon: form.icon,
        color: form.color,
        status: form.status,
        start_date: localInputToIso(form.start_date),
        target_end_date: localInputToIso(form.target_end_date),
        actual_end_date: showActualEnd.value
            ? localInputToIso(form.actual_end_date)
            : null,
        timezone: form.timezone || null,
        agent_enabled: form.agent_enabled,
        default_agent_permission_level: form.default_agent_permission_level,
    };

    emit("submit", payload);
}
</script>

<template>
    <v-form ref="formRef" class="project-form" @submit.prevent="onSubmit">
        <section class="project-form__section">
            <h3 class="project-form__title">Basics</h3>

            <div class="project-form__field">
                <label class="project-form__label" for="project-name"
                    >Name</label
                >
                <v-text-field
                    id="project-name"
                    v-model="form.name"
                    class="project-form__input"
                    variant="outlined"
                    density="compact"
                    placeholder="Project name"
                    :rules="nameRules"
                    autofocus
                    hide-details="auto"
                />
            </div>

            <div class="project-form__field">
                <label class="project-form__label" for="project-description"
                    >Description</label
                >
                <v-textarea
                    id="project-description"
                    v-model="form.description"
                    class="project-form__input"
                    variant="outlined"
                    density="compact"
                    placeholder="What is this project about?"
                    rows="3"
                    auto-grow
                    hide-details="auto"
                />
            </div>
        </section>

        <section class="project-form__section project-form__section--split">
            <div class="project-form__col">
                <h3 class="project-form__title">More</h3>

                <div class="project-form__field">
                    <IconInput
                        v-model="form.icon"
                        variant="icon-and-label"
                        label-color="secondary"
                    />
                </div>
                <div class="project-form__field">
                    <ColorInput
                        v-model="form.color"
                        variant="icon-and-label"
                        label-color="secondary"
                    />
                </div>

                <div class="project-form__field">
                    <label class="project-form__label" for="project-status"
                        >Status</label
                    >
                    <v-select
                        id="project-status"
                        v-model="form.status"
                        class="project-form__input"
                        :items="STATUS_ITEMS"
                        variant="outlined"
                        density="compact"
                        hide-details="auto"
                    />
                </div>
            </div>

            <div class="project-form__col">
                <h3 class="project-form__title">Schedule</h3>

                <div class="project-form__field">
                    <label class="project-form__label" for="project-start"
                        >Start</label
                    >
                    <v-text-field
                        id="project-start"
                        v-model="form.start_date"
                        class="project-form__input"
                        type="datetime-local"
                        variant="outlined"
                        density="compact"
                        clearable
                        hide-details="auto"
                    />
                </div>

                <div class="project-form__field">
                    <label class="project-form__label" for="project-target-end"
                        >Target end</label
                    >
                    <v-text-field
                        id="project-target-end"
                        ref="targetEndRef"
                        v-model="form.target_end_date"
                        class="project-form__input"
                        type="datetime-local"
                        variant="outlined"
                        density="compact"
                        :rules="targetEndRules"
                        clearable
                        hide-details="auto"
                    />
                </div>

                <div v-if="showActualEnd" class="project-form__field">
                    <label class="project-form__label" for="project-actual-end"
                        >Actual end</label
                    >
                    <v-text-field
                        id="project-actual-end"
                        ref="actualEndRef"
                        v-model="form.actual_end_date"
                        class="project-form__input"
                        type="datetime-local"
                        variant="outlined"
                        density="compact"
                        :rules="actualEndRules"
                        clearable
                        hide-details="auto"
                    />
                </div>

                <div class="project-form__field">
                    <label class="project-form__label" for="project-timezone"
                        >Timezone</label
                    >
                    <v-autocomplete
                        id="project-timezone"
                        v-model="form.timezone"
                        class="project-form__input"
                        :items="TIMEZONE_ITEMS"
                        variant="outlined"
                        density="compact"
                        clearable
                        hide-details="auto"
                    />
                </div>
            </div>
        </section>

        <section class="project-form__section">
            <h3 class="project-form__title">Agent</h3>

            <div class="project-form__switch-row">
                <div class="project-form__switch-text">
                    <span class="project-form__label project-form__label--flush"
                        >Enable agent</span
                    >
                    <span class="project-form__hint"
                        >Let the agent work on this project</span
                    >
                </div>
                <v-switch
                    v-model="form.agent_enabled"
                    color="primary"
                    density="compact"
                    inset
                    hide-details
                    aria-label="Enable agent"
                />
            </div>

            <div v-if="form.agent_enabled" class="project-form__field">
                <label class="project-form__label" for="project-permission"
                    >Default permission level</label
                >
                <v-select
                    id="project-permission"
                    v-model="form.default_agent_permission_level"
                    class="project-form__input"
                    :items="PERMISSION_ITEMS"
                    variant="outlined"
                    density="compact"
                    hide-details="auto"
                >
                    <template #item="{ props: itemProps, item }">
                        <v-list-item
                            v-bind="itemProps"
                            :title="item.raw.title"
                            :subtitle="item.raw.subtitle"
                        />
                    </template>
                </v-select>
            </div>
        </section>

        <footer class="project-form__footer">
            <v-btn
                v-ripple
                class="text-none project-form__btn"
                variant="text"
                density="compact"
                @click="emit('cancel')"
            >
                Cancel
            </v-btn>
            <v-btn
                v-ripple
                class="text-none project-form__btn project-form__btn--primary"
                type="submit"
                variant="flat"
                color="primary"
                density="comfortable"
                :loading="loading"
            >
                Create Project
            </v-btn>
        </footer>
    </v-form>
</template>

<style scoped>
.project-form {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 35rem;
    color: rgb(var(--v-theme-on-surface));
}

.project-form__section {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem 0;
    border-top: 0.0625rem solid rgb(var(--v-theme-outline, 225, 228, 232));
}

.project-form__section:first-child {
    padding-top: 0;
    border-top: none;
}

.project-form__section--split {
    gap: 1.5rem;
}

.project-form__col {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    flex: 1 1 0;
    min-width: 0;
}

.project-form__title {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
}

.project-form__row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
}

.project-form__field {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    min-width: 0;
}

.project-form__label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    user-select: none;
    -webkit-user-select: none;
}

.project-form__label--flush {
    color: rgb(var(--v-theme-on-surface));
}

.project-form__hint {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
}

.project-form__switch-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.project-form__switch-text {
    display: flex;
    flex-direction: column;
    gap: 0.125rem;
}

.project-form__footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.25rem;
    padding-top: 1rem;
    border-top: 0.0625rem solid rgb(var(--v-theme-outline, 225, 228, 232));
}

.project-form__btn {
    font-size: 0.8125rem;
    font-weight: 500;
    letter-spacing: normal;
    border-radius: 0.5rem;
    user-select: none;
    -webkit-user-select: none;
}

.project-form__btn--primary {
    border-radius: 0.625rem;
}

:deep(.project-form__input .v-input__details) {
    min-height: 0;
    padding: 0.25rem 0 0;
}

:deep(.project-form__input .v-messages__message) {
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1rem;
}

:deep(.project-form__input .v-field) {
    border-radius: 0.5rem;
    font-size: 0.8125rem;
}

:deep(.project-form__input .v-field--variant-outlined .v-field__outline) {
    --v-field-border-opacity: 1;
    color: rgb(var(--v-theme-outline, 225, 228, 232));
}

:deep(
    .project-form__input .v-field--variant-outlined .v-field__outline__start
) {
    border-radius: 0.5rem 0 0 0.5rem;
}

:deep(.project-form__input .v-field--variant-outlined .v-field__outline__end) {
    border-radius: 0 0.5rem 0.5rem 0;
}

:deep(.project-form__input .v-field--variant-outlined:hover) {
    box-shadow: 0 0 0 0.0625rem rgba(165, 172, 182, 0.5);
}

:deep(.project-form__input .v-field--variant-outlined:hover .v-field__outline) {
    color: rgb(var(--v-theme-outline-variant, 165, 172, 182));
}

:deep(.project-form__input .v-field--variant-outlined.v-field--focused) {
    box-shadow: 0 0 0 0.0625rem rgba(25, 118, 210, 0.15);
}

:deep(
    .project-form__input
        .v-field--variant-outlined.v-field--focused
        .v-field__outline
) {
    color: rgb(var(--v-theme-primary));
}

:deep(
    .project-form__input
        .v-field--variant-outlined.v-field--error
        .v-field__outline
) {
    color: rgb(var(--v-theme-error));
}

:deep(.project-form__input .v-field__input::placeholder) {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    opacity: 1;
}

@media (min-width: 48rem) {
    .project-form__section--split {
        flex-direction: row;
        align-items: flex-start;
    }
}

@media (max-width: 30rem) {
    .project-form__row {
        grid-template-columns: 1fr;
    }
}
</style>
