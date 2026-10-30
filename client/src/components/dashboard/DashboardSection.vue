<script setup>
defineProps({
    title: {
        type: String,
        required: true,
    },
    icon: {
        type: String,
        default: null,
    },
    actionTo: {
        type: Object,
        default: null,
    },
    actionLabel: {
        type: String,
        default: "View all",
    },
});
</script>

<template>
    <section class="dashboard-section">
        <header class="dashboard-section__header">
            <div class="dashboard-section__title-group">
                <v-icon v-if="icon" :icon="icon" size="16" />

                <h2 class="dashboard-section__title">{{ title }}</h2>
            </div>

            <v-btn
                v-if="actionTo"
                :to="actionTo"
                variant="text"
                color="primary"
                density="compact"
                class="text-none"
            >
                {{ actionLabel }}
            </v-btn>
        </header>

        <div class="dashboard-section__body">
            <slot />
        </div>
    </section>
</template>

<style scoped>
.dashboard-section {
    display: flex;
    flex-direction: column;
    min-width: 0;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
}

.dashboard-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    min-height: 2.75rem;
    padding: 0.25rem 0.5rem 0.25rem 1rem;
    border-bottom: 0.0625rem solid
        rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.dashboard-section__title-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: rgb(var(--v-theme-on-surface));
}

.dashboard-section__title {
    margin: 0;
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}

.dashboard-section__body {
    flex: 1;
    padding: 0.5rem;
}
</style>
