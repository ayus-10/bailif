<script setup>
/**
 * @typedef {import("@/types/settings").Settings} Settings
 */

const props = defineProps({
    settings: {
        /**
         * @type {import("vue").PropType<Settings>}
         */
        type: Object,
        required: true,
    },
});
</script>

<template></template>
