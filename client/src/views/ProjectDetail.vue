<script setup>
import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useProjectsStore } from "@/stores/projects.store";

const route = useRoute();
const store = useProjectsStore();

const projectId = computed(() => String(route.params.id ?? "default"));

onMounted(() => {
    store.fetch(projectId.value);
});

watch(projectId, (id) => {
    store.fetch(id);
});

const project = computed(() => store.items[projectId.value]);

const status = computed(() => store.status[projectId.value] ?? "idle");

const error = computed(() => store.errors[projectId.value]);

function retry() {
    store.fetch(projectId.value, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div v-if="status === 'loading'" class="d-flex justify-center py-12">
            <v-progress-circular indeterminate />
        </div>

        <v-alert v-else-if="status === 'error'" type="error" class="mb-4">
            {{ error?.message }}

            <template #append>
                <v-btn size="small" @click="retry">Retry</v-btn>
            </template>
        </v-alert>

        <ProjectHeader v-else-if="project" :project="project" />
    </v-container>
</template>
