<script setup>
defineProps({
    tags: {
        /** @type {import('vue').PropType<String[]>} */
        type: Array,
        default: () => [],
    },
});
</script>

<template>
    <section v-if="tags.length" class="panel">
        <h2 class="panel__label">Tags</h2>
        <div class="tag-list">
            <v-chip
                v-for="tag in tags"
                :key="tag"
                size="small"
                variant="flat"
                class="tag-chip"
                ripple
            >
                {{ tag }}
            </v-chip>
        </div>
    </section>
</template>

<style scoped>
.panel {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    padding: 0.875rem 1rem;
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.panel__label {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
}

.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.375rem;
}

.tag-chip {
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248)) !important;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103)) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: normal !important;
}

.tag-chip:deep(.v-chip__content) {
    user-select: none;
    -webkit-user-select: none;
}

.tag-chip:hover {
    background: color-mix(
        in srgb,
        #1976d2 10%,
        rgb(var(--v-theme-grey-lighten-4, 245, 246, 248))
    ) !important;
    color: #1976d2 !important;
}
</style>
