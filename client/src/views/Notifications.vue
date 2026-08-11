<script setup>
import { computed, onMounted } from "vue";
import NotificationList from "@/components/notifications/NotificationList.vue";
import { useNotificationsStore } from "@/stores/notifications.store";

const store = useNotificationsStore();

const scopeId = "default";

onMounted(() => {
    store.fetch(scopeId);
});

const notifications = computed(() => store.items[scopeId] ?? []);

const status = computed(() => store.status[scopeId] ?? "idle");

const error = computed(() => store.errors[scopeId]);

function retry() {
    store.fetch(scopeId, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Notifications</h1>
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

        <NotificationList v-else :notifications="notifications" />
    </v-container>
</template>
