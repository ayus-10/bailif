<script setup>
/** @typedef {import('@/types/document').Document} Document */

const props = defineProps({
    documents: {
        type: Array,
        default: /** @returns {Document[]} */ () => [],
    },
});
</script>

<template>
    <!-- TODO: document list -->
</template>
