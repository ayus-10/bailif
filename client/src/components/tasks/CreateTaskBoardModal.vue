<script setup>
import { computed, ref } from "vue";

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const colors = [
    "#6366F1",
    "#8B5CF6",
    "#EC4899",
    "#EF4444",
    "#F97316",
    "#EAB308",
    "#22C55E",
    "#14B8A6",
    "#06B6D4",
    "#3B82F6",
];

const form = ref({
    name: "",
    description: "",
    color: colors[0],
});

const canSubmit = computed(() => form.value.name.trim().length > 0);

function close() {
    emit("update:modelValue", false);
}

function submit() {
    if (!canSubmit.value) return;

    emit("submit", {
        name: form.value.name.trim(),
        description: form.value.description.trim() || null,
        color: form.value.color,
    });

    form.value = {
        name: "",
        description: "",
        color: colors[0],
    };

    close();
}
</script>

<template>
    <v-dialog
        :model-value="modelValue"
        max-width="520"
        @update:model-value="emit('update:modelValue', $event)"
    >
        <v-card rounded="xl">
            <v-card-title class="pa-5 pb-2">
                Create task board
            </v-card-title>

            <v-card-text class="pa-5">
                <v-text-field
                    v-model="form.name"
                    label="Name"
                    placeholder="e.g. Product development"
                    variant="outlined"
                    density="comfortable"
                    autofocus
                    hide-details
                    @keyup.enter="submit"
                />

                <v-textarea
                    v-model="form.description"
                    label="Description"
                    placeholder="What is this board for?"
                    variant="outlined"
                    density="comfortable"
                    rows="3"
                    auto-grow
                    hide-details
                    class="mt-4"
                />

                <div class="mt-5">
                    <div class="text-subtitle-2 mb-2">
                        Color
                    </div>

                    <div class="d-flex flex-wrap ga-2">
                        <button
                            v-for="color in colors"
                            :key="color"
                            type="button"
                            class="color-option"
                            :class="{
                                'color-option--selected':
                                    form.color === color,
                            }"
                            :style="{ '--color': color }"
                            :aria-label="`Select ${color}`"
                            :aria-pressed="form.color === color"
                            @click="form.color = color"
                        >
                            <v-icon
                                v-if="form.color === color"
                                icon="mdi-check"
                                size="18"
                            />
                        </button>
                    </div>
                </div>
            </v-card-text>

            <v-card-actions class="pa-5 pt-0">
                <v-spacer />

                <v-btn variant="text" @click="close">
                    Cancel
                </v-btn>

                <v-btn
                    color="primary"
                    variant="flat"
                    :disabled="!canSubmit"
                    @click="submit"
                >
                    Create board
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
.color-option {
    width: 36px;
    height: 36px;
    border: 2px solid transparent;
    border-radius: 50%;
    background: var(--color);
    color: white;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition:
        transform 120ms ease,
        box-shadow 120ms ease;
}

.color-option:hover {
    transform: scale(1.08);
}

.color-option--selected {
    border-color: rgb(var(--v-theme-on-surface));
    box-shadow: 0 0 0 2px rgb(var(--v-theme-surface));
}

.color-option:focus-visible {
    outline: 2px solid rgb(var(--v-theme-primary));
    outline-offset: 2px;
}
</style>
