<script setup>
/** @typedef {import("@/types/notification").Notification} Notification */

const props = defineProps({
    notifications: {
        type: Array,
        default: /** @returns {Notification[]} */ () => [],
    },
});
</script>

<template></template>
