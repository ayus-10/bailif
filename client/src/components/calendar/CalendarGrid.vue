<script setup>
/** @typedef {import('@/types/calendar').CalendarEvent} CalendarEvent */

const props = defineProps({
    events: {
        type: Array,
        default: /** @returns {CalendarEvent[]} */ () => [],
    },
});
</script>

<template>
    <!-- TODO: calendar grid -->
</template>
