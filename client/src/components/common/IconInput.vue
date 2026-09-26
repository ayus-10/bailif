<script setup>
import { computed } from "vue";
import { DEFAULT_ICONS } from "@/constants/globals";

/**
 * @typedef {import("@/constants/globals").IconOption} IconOption
 */

const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
    icons: {
        /**
         * @type {import("vue").PropType<IconOption[]>}
         */
        type: Array,
        default: () => DEFAULT_ICONS,
    },
    label: {
        type: String,
        default: "Icon",
    },
    labelColor: {
        type: String,
        default: "primary",
        validator: (/** @type {string} */ value) =>
            ["primary", "secondary"].includes(value),
    },
    variant: {
        type: String,
        default: "icon-only",
        validator: (/** @type {string} */ value) =>
            ["icon-only", "icon-and-label"].includes(value),
    },
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const selectedIcon = computed(() => {
    if (!props.modelValue) return null;
    return props.icons.find(
        (icon) =>
            (typeof icon === "string" ? icon : icon.value) === props.modelValue
    );
});

/**
 * @param {string} icon
 */
function selectIcon(icon) {
    if (props.disabled) return;
    emit("update:modelValue", icon);
}

/**
 * @param {IconOption} icon
 */
function getIconValue(icon) {
    return typeof icon === "string" ? icon : icon.value;
}

/**
 * @param {IconOption} icon
 */
function getIconLabel(icon) {
    return typeof icon === "string" ? icon : icon.label || icon.value;
}
</script>

<template>
    <div class="icon-input-wrapper">
        <label
            v-if="label"
            class="field-label"
            :class="`field-label__${labelColor}`"
        >
            {{ label }}
        </label>

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
                    :class="{
                        'icon-trigger-btn--with-label':
                            variant === 'icon-and-label',
                    }"
                    :aria-label="
                        selectedIcon
                            ? `Selected icon: ${getIconLabel(selectedIcon)}`
                            : 'Choose an icon'
                    "
                >
                    <v-icon
                        v-if="modelValue"
                        :icon="modelValue"
                        size="18"
                        class="icon-preview"
                    />
                    <v-icon
                        v-else
                        icon="mdi-shape-outline"
                        size="18"
                        class="icon-preview-placeholder text-medium-emphasis"
                    />

                    <span
                        v-if="variant === 'icon-and-label' && selectedIcon"
                        class="icon-trigger-label"
                    >
                        {{ getIconLabel(selectedIcon) }}
                    </span>

                    <v-icon
                        icon="mdi-chevron-down"
                        size="14"
                        class="chevron-icon text-medium-emphasis"
                    />
                </button>
            </template>

            <v-card class="icon-picker-card" variant="outlined">
                <div class="icon-grid" role="radiogroup" :aria-label="label">
                    <button
                        v-for="icon in icons"
                        :key="getIconValue(icon)"
                        type="button"
                        class="icon-grid-item"
                        :class="{
                            'icon-grid-item--selected':
                                modelValue === getIconValue(icon),
                        }"
                        :aria-label="`Select ${getIconLabel(icon)}`"
                        :aria-checked="modelValue === getIconValue(icon)"
                        role="radio"
                        @click="selectIcon(getIconValue(icon))"
                    >
                        <v-icon
                            :icon="getIconValue(icon)"
                            size="18"
                            class="icon-item-symbol"
                        />
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
    margin-bottom: 0.375rem;
}

.field-label__primary {
    color: var(--v-theme-on-surface-variant, #344054);
}

.field-label__secondary {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
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

.icon-trigger-btn--with-label {
    width: 100%;
    justify-content: flex-start;
    padding: 0 0.625rem;
}

.icon-trigger-label {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1.25rem;
    text-align: left;
    text-overflow: ellipsis;
    white-space: nowrap;
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

.icon-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgb(var(--v-theme-on-surface));
}

.icon-preview-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
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
    max-width: 18rem;
}

.icon-grid-item {
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
    color: var(--v-theme-on-surface-variant, #475467);
    transition:
        background-color 0.15s ease,
        border-color 0.15s ease,
        color 0.15s ease;
}

.icon-grid-item:hover {
    background-color: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-on-surface, #101828);
}

.icon-item-symbol {
    display: flex;
    align-items: center;
    justify-content: center;
}

.icon-grid-item--selected {
    border-color: var(--v-theme-outline-dark, #98a2b3);
    background-color: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-primary, #1976d2);
}
</style>
