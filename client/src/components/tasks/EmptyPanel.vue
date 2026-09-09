<script setup>
defineProps({
    icon: {
        type: String,
        default: "mdi-plus",
    },
    message: {
        type: String,
        default: "Nothing here yet - click to add some",
    },
});

const emit = defineEmits(["click"]);
</script>

<template>
    <button type="button" class="panel__empty" @click="emit('click')">
        <v-icon :icon="icon" size="16" />
        <span>{{ message }}</span>
    </button>
</template>

<style scoped>
.panel__empty {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    width: 100%;
    padding: 0.75rem;
    border: 0.0625rem dashed rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.625rem;
    background: transparent;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition:
        border-color 0.12s ease,
        color 0.12s ease;
}

.panel__empty:hover {
    border-color: rgba(25, 118, 210, 0.35);
    color: #1976d2;
}
</style>
