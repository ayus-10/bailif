<script setup>
import { computed } from "vue";
import { DEFAULT_COLORS } from "@/constants/globals";

/** @typedef {import('@/constants/globals').ColorOption} ColorOption */

const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
    colors: {
        /** @type {import('vue').PropType<ColorOption[]>} */
        type: Array,
        default: () => DEFAULT_COLORS,
    },
    label: {
        type: String,
        default: "Color",
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const selectedColor = computed(() => {
    if (!props.modelValue) return null;
    return props.colors.find(
        (c) => (typeof c === "string" ? c : c.value) === props.modelValue
    );
});

/** @param {string} color */
function selectColor(color) {
    if (props.disabled) return;
    emit("update:modelValue", color);
}

/** @param {ColorOption} color */
function getColorValue(color) {
    return typeof color === "string" ? color : color.value;
}

/** @param {ColorOption} color */
function getColorLabel(color) {
    return typeof color === "string" ? color : color.label || color.value;
}
</script>

<template>
    <div class="color-input-wrapper">
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
                    class="color-trigger-btn"
                    :aria-label="
                        selectedColor
                            ? `Selected color: ${getColorLabel(selectedColor)}`
                            : 'Choose a color'
                    "
                >
                    <span
                        v-if="modelValue"
                        class="color-preview-swatch"
                        :style="{ backgroundColor: modelValue }"
                    />
                    <span v-else class="color-preview-placeholder" />

                    <v-icon
                        icon="mdi-chevron-down"
                        size="14"
                        class="chevron-icon text-medium-emphasis"
                    />
                </button>
            </template>

            <v-card class="color-picker-card" variant="outlined">
                <div class="color-grid" role="radiogroup" :aria-label="label">
                    <button
                        v-for="color in colors"
                        :key="getColorValue(color)"
                        type="button"
                        class="color-grid-item"
                        :class="{
                            'color-grid-item--selected':
                                modelValue === getColorValue(color),
                        }"
                        :style="{ '--swatch-color': getColorValue(color) }"
                        :aria-label="`Select ${getColorLabel(color)}`"
                        :aria-checked="modelValue === getColorValue(color)"
                        role="radio"
                        @click="selectColor(getColorValue(color))"
                    >
                        <span class="color-swatch-circle" />
                        <v-icon
                            v-if="modelValue === getColorValue(color)"
                            icon="mdi-check"
                            size="14"
                            class="check-icon"
                        />
                    </button>
                </div>
            </v-card>
        </v-menu>
    </div>
</template>

<style scoped>
:deep(.color-picker-card.v-card) {
    background-color: rgb(var(--v-theme-surface)) !important;
    border: 0.0625rem solid rgb(var(--v-theme-outline));
    border-radius: 0.375rem;
    box-shadow: none;
    padding: 0.5rem;
    margin-top: 0.25rem;
}

.color-input-wrapper {
    display: flex;
    flex-direction: column;
}

.field-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: var(--v-theme-on-surface-variant, #344054);
    margin-bottom: 0.375rem;
}

.color-trigger-btn {
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

.color-trigger-btn:hover:not(:disabled) {
    border-color: var(--v-theme-outline-dark, #98a2b3);
}

.color-trigger-btn:focus-visible {
    outline: 0.125rem solid var(--v-theme-primary, #1976d2);
    outline-offset: 0.0625rem;
}

.color-trigger-btn:disabled {
    background-color: var(--v-theme-surface-disabled, #f2f4f7);
    border-color: var(--v-theme-outline-disabled, #eaecf0);
    cursor: not-allowed;
}

.color-preview-swatch {
    width: 1.25rem;
    height: 1.25rem;
    border-radius: 50%;
    border: 0.0625rem solid rgba(0, 0, 0, 0.12);
}

.color-preview-placeholder {
    width: 1.25rem;
    height: 1.25rem;
    border-radius: 50%;
    border: 0.0625rem dashed var(--v-theme-outline, #d0d5dd);
    background-color: transparent;
}

.color-picker-card.v-card {
    background-color: var(--v-theme-surface, #ffffff);
    border: 0.0625rem solid var(--v-theme-outline, #e1e4e8);
    border-radius: 0.375rem;
    box-shadow: none;
    padding: 0.5rem;
    margin-top: 0.25rem;
}

.color-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.25rem;
    width: 100%;
    max-width: 12.5rem;
}

.color-grid-item {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.125rem;
    height: 2.125rem;
    border-radius: 0.25rem;
    border: 0.0625rem solid transparent;
    background: transparent;
    cursor: pointer;
}

.color-grid-item:hover {
    background-color: var(--v-theme-surface-variant, #f8f9fa);
}

.color-swatch-circle {
    width: 1.25rem;
    height: 1.25rem;
    border-radius: 50%;
    background-color: var(--swatch-color);
    border: 0.0625rem solid rgba(0, 0, 0, 0.12);
}

.color-grid-item--selected {
    border-color: var(--v-theme-outline-dark, #98a2b3);
    background-color: var(--v-theme-surface-variant, #f8f9fa);
}

.check-icon {
    position: absolute;
    color: #ffffff;
    filter: drop-shadow(0 0 0.0625rem rgba(0, 0, 0, 0.75));
}
</style>
