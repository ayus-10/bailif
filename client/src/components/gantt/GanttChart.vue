<script setup>
/** @typedef {import('@/types/gantt').GanttTask} GanttTask */

const props = defineProps({
    tasks: {
        type: Array,
        default: /** @returns {GanttTask[]} */ () => [],
    },
});
</script>

<template>
    <!-- TODO: gantt chart -->
</template>
