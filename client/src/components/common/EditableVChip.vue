<script setup>
import { computed, ref, watch } from "vue";

/** @typedef {{ value: string, label: string, color: string, icon: string }} SelectOption */

const props = defineProps({
    items: {
        /** @type {import("vue").PropType<SelectOption[]>} */
        type: Array,
        required: true,
        validator: (
            /** @type {SelectOption[]} */
            items
        ) =>
            items.every((item) =>
                ["value", "label", "color", "icon"].every((key) => key in item)
            ),
    },
    modelValue: {
        type: [String, Number],
        default: undefined,
    },
    defaultValue: {
        type: [String, Number],
        default: undefined,
    },
    size: {
        type: String,
        default: "small",
    },
    rounded: {
        type: /** @type {import("vue").PropType<"0" | "sm" | "lg" | "pill" | "xl">} */ (
            String
        ),
        default: "pill",
    },
    variant: {
        type: /** @type {import("vue").PropType<"tonal" | "flat" | "text" | "elevated" | "outlined" | "plain">} */ (
            String
        ),
        default: "tonal",
        validator: (
            /** @type {String} */
            value
        ) =>
            ["tonal", "flat", "text", "elevated", "outlined", "plain"].includes(
                value
            ),
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    placeholder: {
        type: String,
        default: "Select",
    },
});

const emit = defineEmits(["update:modelValue", "change"]);

const menuOpen = ref(false);

const internalValue = ref(
    props.modelValue ?? props.defaultValue ?? props.items[0]?.value
);

// Keep in sync if the parent drives modelValue externally.
watch(
    () => props.modelValue,
    (val) => {
        if (val !== undefined && val !== internalValue.value) {
            internalValue.value = val;
        }
    }
);

const selected = computed(() =>
    props.items.find((i) => i.value === internalValue.value)
);

/** @param {SelectOption} item */
function selectItem(item) {
    if (props.disabled) return;
    menuOpen.value = false;
    if (item.value === internalValue.value) return;

    internalValue.value = item.value;
    emit("update:modelValue", item.value);
    emit("change", item);
}
</script>

<template>
    <v-menu
        v-model="menuOpen"
        :close-on-content-click="true"
        :disabled="disabled"
        location="bottom start"
    >
        <template #activator="{ props: activatorProps }">
            <v-chip
                v-bind="activatorProps"
                :size="size"
                :variant="variant"
                :rounded="rounded"
                :color="selected?.color"
                :prepend-icon="selected?.icon"
                :disabled="disabled"
                class="editable-v-chip"
                :class="{ 'editable-v-chip--editable': !disabled }"
            >
                {{ selected?.label ?? placeholder }}
                <v-icon
                    v-if="!disabled"
                    icon="mdi-menu-down"
                    size="x-small"
                    class="editable-v-chip__caret"
                />
            </v-chip>
        </template>
        <v-list density="compact" min-width="180" class="editable-v-chip-list">
            <v-list-item
                v-for="item in items"
                :key="item.value"
                :active="item.value === internalValue"
                class="editable-v-chip-list__item"
                @click="selectItem(item)"
            >
                <template #prepend>
                    <v-icon
                        :icon="item.icon"
                        :color="item.color"
                        size="small"
                        class="mr-2"
                    />
                </template>
                <v-list-item-title :class="`text-${item.color}`">
                    {{ item.label }}
                </v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>

<style scoped>
.editable-v-chip {
    font-weight: 600;
    letter-spacing: normal;
    user-select: none;
    -webkit-user-select: none;
    transition:
        background-color 0.12s ease,
        box-shadow 0.12s ease;
}

.editable-v-chip--editable {
    cursor: pointer;
}

.editable-v-chip--editable:hover {
    box-shadow: inset 0 0 0 0.0625rem currentColor;
}

.editable-v-chip__caret {
    margin-left: 0.125rem;
    opacity: 0.7;
}

.editable-v-chip-list {
    border-radius: 0.625rem !important;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.editable-v-chip-list__item {
    border-radius: 0.5rem !important;
    margin: 0.125rem 0.375rem;
}
</style>
