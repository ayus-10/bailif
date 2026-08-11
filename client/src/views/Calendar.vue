<script setup>
import { computed, onMounted } from "vue";
import CalendarGrid from "@/components/calendar/CalendarGrid.vue";
import { useCalendarStore } from "@/stores/calendar.store";

const store = useCalendarStore();

const monthKey = computed(() => {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
});

onMounted(() => {
    store.fetch(monthKey.value);
});

const calendar = computed(() => store.items[monthKey.value]);

const status = computed(() => store.status[monthKey.value] ?? "idle");

const error = computed(() => store.errors[monthKey.value]);

function retry() {
    store.fetch(monthKey.value, { force: true });
}
</script>

<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <h1 class="text-h5 font-weight-medium">Calendar</h1>
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

        <CalendarGrid v-else :events="calendar?.events ?? []" />
    </v-container>
</template>
