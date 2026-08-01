<script setup>
import { computed, onMounted } from "vue";

import DashboardMetrics from "@/components/dashboard/DashboardMetrics.vue";
import { useDashboardStore } from "@/stores/dashboard.store";

const store = useDashboardStore();

const scopeId = "default";

onMounted(() => {
    store.fetch(scopeId);
});

const dashboard = computed(() => store.items[scopeId]);

const status = computed(() => store.status[scopeId] ?? "idle");

const error = computed(() => store.errors[scopeId]);

function retry() {
    store.fetch(scopeId, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-6">
            <div>
                <h1 class="text-h5 font-weight-medium">Dashboard</h1>
                <span class="text-body-2 text-medium-emphasis">
                    Here's what's happening across your projects
                </span>
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

        <DashboardMetrics v-else :metrics="dashboard?.metrics ?? []" />
    </v-container>
</template>
