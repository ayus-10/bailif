<script setup>
/** @typedef {import('@/types/project').ProjectRead} ProjectRead */

const props = defineProps({
    project: {
        /** @type {import('vue').PropType<ProjectRead>} */
        type: Object,
        required: true,
    },
});
</script>

<template>
    <!-- TODO: project header -->
</template>
