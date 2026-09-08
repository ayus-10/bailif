<script setup>
/** @typedef {import("@/types/task").TaskRead} TaskRead */

defineProps({
    task: {
        /** @type {import("vue").PropType<TaskRead>} */
        type: Object,
        required: true,
    },
});

const emit = defineEmits(["back"]);
</script>

<template>
    <div class="task-page__breadcrumbs">
        <v-btn
            icon="mdi-arrow-left"
            variant="text"
            density="comfortable"
            aria-label="Go back"
            @click="emit('back')"
        />

        <span>Dashboard</span>
        <v-icon icon="mdi-chevron-right" size="16" />
        <span>Tasks</span>
        <v-icon icon="mdi-chevron-right" size="16" />

        <span class="task-page__breadcrumb-current">
            <!-- TODO: replace with an identifier -->
            {{ task.id }}
        </span>
    </div>
</template>

<style scoped>
.task-page__breadcrumbs {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--tp-ink-muted);
    font-size: 0.8125rem;
    font-weight: 500;
}

.task-page__breadcrumb-current {
    color: var(--tp-ink);
    font-weight: 600;
}
</style>
