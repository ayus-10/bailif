<script setup>
import { useRoute } from "vue-router";
import { computed, onMounted, watch } from "vue";
import ProjectHeader from "@/components/projects/ProjectHeader.vue";
import { useProjectsStore } from "@/stores/projects.store";

const route = useRoute();
const store = useProjectsStore();

const projectId = computed(() => String(route.params.id));

onMounted(() => {
    store.get(projectId.value);
});

watch(projectId, (id) => {
    store.get(id);
});

const project = computed(() => store.currentProject);

const status = computed(() => store.status);

const error = computed(() => store.error);

function retry() {
    store.get(projectId.value, { forceRefresh: true });
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
