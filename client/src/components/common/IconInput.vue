<script setup>
import { computed } from "vue";
import { DEFAULT_ICONS } from "@/constants/globals";

/** @typedef {import('@/constants/globals').IconOption} IconOption */

const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
    icons: {
        /** @type {import("vue").PropType<IconOption[]>} */
        type: Array,
        default: () => DEFAULT_ICONS,
    },
    label: {
        type: String,
        default: "Icon",
    },
    size: {
        type: [Number, String],
        default: 42,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const selectedIcon = computed(() =>
    props.icons.find((icon) => icon.value === props.modelValue)
);

/** @param {string} icon */
function selectIcon(icon) {
    if (props.disabled) return;

    emit("update:modelValue", icon);
}
</script>

<template>
    <div class="icon-input-wrapper">
        <label v-if="label" class="field-label">{{ label }}</label>

        <v-menu
            :disabled="disabled"
            :close-on-content-click="true"
            location="bottom start"
        >
            <template #activator="{ props: menuProps }">
                <button
                    type="button"
                    v-bind="menuProps"
                    :disabled="disabled"
                    class="icon-trigger-btn"
                    :aria-label="
                        selectedIcon
                            ? `Selected icon: ${selectedIcon.label}`
                            : 'Choose an icon'
                    "
                >
                    <v-icon
                        v-if="selectedIcon"
                        :icon="selectedIcon.value"
                        size="20"
                        color="primary"
                    />
                    <v-icon
                        v-else
                        icon="mdi-shape-outline"
                        size="18"
                        class="text-medium-emphasis"
                    />

                    <v-icon
                        icon="mdi-chevron-down"
                        size="14"
                        class="chevron-icon text-medium-emphasis"
                    />
                </button>
            </template>

            <v-card class="icon-picker-card" variant="outlined">
                <div class="icon-grid">
                    <button
                        v-for="icon in icons"
                        :key="icon.value"
                        type="button"
                        class="icon-grid-item"
                        :class="{
                            'icon-grid-item--selected':
                                modelValue === icon.value,
                        }"
                        :aria-label="icon.label"
                        :aria-pressed="modelValue === icon.value"
                        @click="selectIcon(icon.value)"
                    >
                        <v-icon :icon="icon.value" size="20" />
                    </button>
                </div>
            </v-card>
        </v-menu>
    </div>
</template>

<style scoped>
:deep(.icon-picker-card.v-card) {
    background-color: rgb(var(--v-theme-surface)) !important;
    border: 0.0625rem solid rgb(var(--v-theme-outline));
    border-radius: 0.375rem;
    box-shadow: none;
    padding: 0.5rem;
    margin-top: 0.25rem;
}

.icon-input-wrapper {
    display: flex;
    flex-direction: column;
}

.field-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: var(--v-theme-on-surface-variant, #344054);
    margin-bottom: 0.375rem;
}

.icon-trigger-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    width: 3.25rem;
    height: 2.375rem;
    background-color: var(--v-theme-surface, #ffffff);
    border: 0.0625rem solid var(--v-theme-outline, #d0d5dd);
    border-radius: 0.375rem;
    cursor: pointer;
    padding: 0 0.375rem;
    transition: border-color 0.15s ease;
}

.icon-trigger-btn:hover:not(:disabled) {
    border-color: var(--v-theme-outline-dark, #98a2b3);
}

.icon-trigger-btn:focus-visible {
    outline: 0.125rem solid var(--v-theme-primary, #1976d2);
    outline-offset: 0.0625rem;
}

.icon-trigger-btn:disabled {
    background-color: var(--v-theme-surface-disabled, #f2f4f7);
    border-color: var(--v-theme-outline-disabled, #eaecf0);
    cursor: not-allowed;
}

.icon-picker-card.v-card {
    background-color: var(--v-theme-surface, #ffffff);
    border: 0.0625rem solid var(--v-theme-outline, #e1e4e8);
    border-radius: 0.375rem;
    box-shadow: none;
    padding: 0.5rem;
    margin-top: 0.25rem;
}

.icon-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.25rem;
    width: 100%;
    max-width: 12.5rem;
}

.icon-grid-item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.125rem;
    height: 2.125rem;
    border-radius: 0.25rem;
    border: 0.0625rem solid transparent;
    background: transparent;
    color: var(--v-theme-on-surface-variant, #475467);
    cursor: pointer;
}

.icon-grid-item:hover {
    background-color: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface, #101828);
}

.icon-grid-item--selected {
    color: var(--v-theme-primary, #1976d2);
    background-color: rgba(var(--v-theme-primary, 25, 118, 210), 0.08);
    border-color: rgba(var(--v-theme-primary, 25, 118, 210), 0.3);
}
</style>
