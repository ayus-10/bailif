<script setup>
/**
 * @typedef {import("@/types/dashboard").DashboardMetric} DashboardMetric
 */

defineProps({
    metrics: {
        type: Array,
        default: /** @returns {DashboardMetric[]} */ () => [],
    },
});
</script>

<template>
    <div class="dashboard-metrics">
        <div
            v-for="metric in metrics"
            :key="metric.key"
            class="dashboard-metric"
            :class="{ 'dashboard-metric--alert': metric.isAlert }"
        >
            <div class="dashboard-metric__icon" aria-hidden="true">
                <v-icon :icon="metric.icon" size="18" />
            </div>

            <div class="dashboard-metric__content">
                <span class="dashboard-metric__value">{{ metric.value }}</span>

                <span class="dashboard-metric__label">{{ metric.label }}</span>

                <span v-if="metric.caption" class="dashboard-metric__caption">
                    {{ metric.caption }}
                </span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dashboard-metrics {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}

.dashboard-metric {
    --metric-accent: rgb(var(--v-theme-primary));

    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    min-width: 0;
    padding: 1rem;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
}

.dashboard-metric--alert {
    --metric-accent: rgb(var(--v-theme-error));
}

.dashboard-metric__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    border-radius: 0.5rem;
    background: color-mix(
        in srgb,
        var(--metric-accent) 10%,
        rgb(var(--v-theme-surface))
    );
    color: var(--metric-accent);
}

.dashboard-metric__content {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.dashboard-metric__value {
    color: rgb(var(--v-theme-on-surface));
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.75rem;
}

.dashboard-metric__label {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    line-height: 1.25rem;
}

.dashboard-metric__caption {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.75rem;
    line-height: 1rem;
}

@media (min-width: 960px) {
    .dashboard-metrics {
        grid-template-columns: repeat(5, minmax(0, 1fr));
    }
}
</style>
