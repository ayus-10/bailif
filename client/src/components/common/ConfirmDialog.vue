<script setup>
defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        required: true,
    },
    message: {
        type: String,
        required: true,
    },
    confirmLabel: {
        type: String,
        default: "Delete",
    },
    loading: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue", "confirm"]);
</script>

<template>
    <v-dialog
        :model-value="modelValue"
        max-width="26rem"
        @update:model-value="emit('update:modelValue', $event)"
    >
        <v-card variant="outlined" rounded="lg" class="pa-5">
            <h2 class="text-h6 font-weight-bold">{{ title }}</h2>

            <p class="text-body-2 text-medium-emphasis mt-2">{{ message }}</p>

            <v-card-actions class="px-0 pt-4 pb-0">
                <v-spacer />

                <v-btn
                    variant="text"
                    class="text-none"
                    :disabled="loading"
                    @click="emit('update:modelValue', false)"
                >
                    Cancel
                </v-btn>

                <v-btn
                    color="error"
                    variant="flat"
                    class="text-none"
                    :loading="loading"
                    @click="emit('confirm')"
                >
                    {{ confirmLabel }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<style scoped>
.v-card {
    background-color: #fff;
    border: 1px solid rgb(var(--v-theme-outline, 225, 228, 232));
    box-shadow: none;
}

.text-h6 {
    color: rgb(var(--v-theme-on-surface));
    line-height: 1.2;
    letter-spacing: -0.01em;
}

:deep(.v-btn) {
    border-radius: 0.375rem;
    box-shadow: none;
}
</style>
