<script setup>
import { computed, onMounted } from "vue";

import DocumentList from "@/components/documents/DocumentList.vue";
import { useDocumentsStore } from "@/stores/documents.store";

const store = useDocumentsStore();

const scopeId = "default";

onMounted(() => {
    store.fetch(scopeId);
});

const documents = computed(() => store.items[scopeId] ?? []);

const status = computed(() => store.status[scopeId] ?? "idle");

const error = computed(() => store.errors[scopeId]);

function retry() {
    store.fetch(scopeId, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-0 fill-height">
        <div v-if="status === 'loading'" class="d-flex justify-center py-12">
            <v-progress-circular indeterminate />
        </div>

        <v-alert v-else-if="status === 'error'" type="error" class="ma-6">
            {{ error?.message }}

            <template #append>
                <v-btn size="small" @click="retry">Retry</v-btn>
            </template>
        </v-alert>

        <DocumentList v-else :documents="documents" />
    </v-container>
</template>
