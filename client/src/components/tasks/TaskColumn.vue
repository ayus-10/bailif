<script setup>
import TaskCard from "./TaskCard.vue";

/** @typedef {import('@/types/task').TaskRead} TaskRead */

defineProps({
    column: {
        type: Object,
        required: true,
    },
    tasks: {
        /** @type {import('vue').PropType<TaskRead[]>} */
        type: Array,
        required: true,
    },
});
</script>

<template>
    <v-col cols="12" md="4">
        <div class="d-flex align-center mb-2">
            <v-icon :icon="column.icon" size="18" class="mr-2" />

            <span class="text-subtitle-2 font-weight-medium">
                {{ column.label }}
            </span>

            <v-chip size="x-small" class="ml-2">
                {{ tasks.length }}
            </v-chip>
        </div>

        <TaskCard v-for="task in tasks" :key="task.id" :task="task" />

        <v-sheet
            v-if="tasks.length === 0"
            class="pa-4 text-center text-caption text-medium-emphasis"
            border
            rounded
        >
            No tasks here
        </v-sheet>
    </v-col>
</template>
