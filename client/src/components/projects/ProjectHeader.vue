<script setup>
/** @typedef {import('@/types/project').Project} Project */

const props = defineProps({
    project: {
        /** @type {import('vue').PropType<Project>} */
        type: Object,
        required: true,
    },
});
</script>

<template>
    <!-- TODO: project header -->
</template>
