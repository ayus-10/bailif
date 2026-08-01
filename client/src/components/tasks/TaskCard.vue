<script setup>
import { PRIORITY_COLORS } from "@/constants/tasks";

/** @typedef {import('@/types/task').TaskRead} TaskRead */

const props = defineProps({
    task: {
        /** @type {import('vue').PropType<TaskRead>} */
        type: Object,
        required: true,
    },
});
</script>

<template>
    <v-card variant="outlined" class="mb-3 pa-3">
        <div class="d-flex justify-space-between align-start">
            <span class="text-body-2 font-weight-medium">
                {{ task.title }}
            </span>

            <v-chip
                :color="PRIORITY_COLORS[task.priority] ?? 'default'"
                size="x-small"
                variant="tonal"
            >
                {{ task.priority }}
            </v-chip>
        </div>

        <div class="text-caption text-medium-emphasis mt-2 d-flex align-center">
            <v-icon icon="mdi-folder-outline" size="14" class="mr-1" />

            {{ task.project }}

            <v-spacer />

            <v-icon icon="mdi-calendar-blank-outline" size="14" class="mr-1" />

            {{ task.due }}
        </div>
    </v-card>
</template>
