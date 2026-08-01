<script setup>
/** @typedef {import('@/types/dashboard').DashboardMetric} DashboardMetric */

const props = defineProps({
    metrics: {
        type: Array,
        default: /** @returns {DashboardMetric[]} */ () => [],
    },
});
</script>

<template>
    <!-- TODO: dashboard metrics -->
</template>
