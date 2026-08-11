<script setup>
import { computed, onMounted } from "vue";
import GanttChart from "@/components/gantt/GanttChart.vue";
import { useGanttStore } from "@/stores/gantt.store";

const store = useGanttStore();

const projectId = "default";

onMounted(() => {
    store.fetch(projectId);
});

const gantt = computed(() => store.items[projectId]);

const status = computed(() => store.status[projectId] ?? "idle");

const error = computed(() => store.errors[projectId]);

function retry() {
    store.fetch(projectId, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Gantt Chart</h1>
            </div>
        </div>

        <div v-if="status === 'loading'" class="d-flex justify-center py-12">
            <v-progress-circular indeterminate />
        </div>

        <v-alert v-else-if="status === 'error'" type="error" class="mb-4">
            {{ error?.message }}

            <template #append>
                <v-btn size="small" @click="retry">Retry</v-btn>
            </template>
        </v-alert>

        <GanttChart v-else :tasks="gantt?.tasks ?? []" />
    </v-container>
</template>
