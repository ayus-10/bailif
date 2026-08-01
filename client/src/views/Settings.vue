<script setup>
import { computed, onMounted } from "vue";

import SettingsPanel from "@/components/settings/SettingsPanel.vue";
import { useSettingsStore } from "@/stores/settings.store";

const store = useSettingsStore();

const scopeId = "default";

onMounted(() => {
    store.fetch(scopeId);
});

const settings = computed(() => store.items[scopeId]);

const status = computed(() => store.status[scopeId] ?? "idle");

const error = computed(() => store.errors[scopeId]);

function retry() {
    store.fetch(scopeId, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <h1 class="text-h5 font-weight-medium mb-6">Settings</h1>

        <div v-if="status === 'loading'" class="d-flex justify-center py-12">
            <v-progress-circular indeterminate />
        </div>

        <v-alert v-else-if="status === 'error'" type="error" class="mb-4">
            {{ error?.message }}

            <template #append>
                <v-btn size="small" @click="retry">Retry</v-btn>
            </template>
        </v-alert>

        <SettingsPanel v-else-if="settings" :settings="settings" />
    </v-container>
</template>
