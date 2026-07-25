<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <h1 class="text-h5 font-weight-medium">Calendar</h1>
            <v-spacer />
            <v-btn icon="mdi-chevron-left" variant="text" @click="shiftMonth(-1)" />
            <span class="text-subtitle-1 mx-2" style="min-width: 160px; text-align: center;">
                {{ monthLabel }}
            </span>
            <v-btn icon="mdi-chevron-right" variant="text" @click="shiftMonth(1)" />
            <v-btn variant="outlined" class="ml-4" @click="goToday">Today</v-btn>
        </div>

        <v-card variant="outlined">
            <div class="calendar-weekdays">
                <span v-for="day in weekdayLabels" :key="day">{{ day }}</span>
            </div>
            <v-divider />
            <div class="calendar-grid">
                <div
                    v-for="cell in calendarCells"
                    :key="cell.key"
                    class="calendar-cell"
                    :class="{ 'calendar-cell--muted': !cell.inMonth, 'calendar-cell--today': cell.isToday }"
                >
                    <span class="text-caption">{{ cell.day }}</span>
                    <div class="calendar-events">
                        <v-chip
                            v-for="event in cell.events"
                            :key="event.id"
                            :color="priorityColor(event.priority)"
                            size="x-small"
                            variant="tonal"
                            class="mb-1"
                            style="width: 100%;"
                        >
                            {{ event.title }}
                        </v-chip>
                    </div>
                </div>
            </div>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const weekdayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Mock deadlines, keyed by ISO date string (YYYY-MM-DD). Swap for a real
// task/query lookup once Task Board and Projects share a data source.
const deadlines = {
    "2026-07-25": [{ id: 1, title: "Finalize wireframes", priority: "high" }],
    "2026-07-28": [{ id: 2, title: "Approve campaign copy", priority: "low" }],
    "2026-07-29": [{ id: 3, title: "Staging environment", priority: "medium" }],
    "2026-08-01": [{ id: 4, title: "Auth flow", priority: "high" }],
    "2026-08-02": [{ id: 5, title: "QA pass", priority: "low" }],
};

const today = new Date();
const viewDate = ref(new Date(today.getFullYear(), today.getMonth(), 1));

const monthLabel = computed(() =>
    viewDate.value.toLocaleDateString(undefined, { month: "long", year: "numeric" })
);

function shiftMonth(delta) {
    viewDate.value = new Date(viewDate.value.getFullYear(), viewDate.value.getMonth() + delta, 1);
}

function goToday() {
    viewDate.value = new Date(today.getFullYear(), today.getMonth(), 1);
}

function toISODate(date) {
    return date.toISOString().slice(0, 10);
}

const calendarCells = computed(() => {
    const year = viewDate.value.getFullYear();
    const month = viewDate.value.getMonth();

    const firstOfMonth = new Date(year, month, 1);
    const startOffset = firstOfMonth.getDay(); // days to back up to Sunday
    const gridStart = new Date(year, month, 1 - startOffset);

    const cells = [];
    for (let i = 0; i < 42; i++) {
        const date = new Date(gridStart.getFullYear(), gridStart.getMonth(), gridStart.getDate() + i);
        const iso = toISODate(date);
        cells.push({
            key: iso,
            day: date.getDate(),
            inMonth: date.getMonth() === month,
            isToday: iso === toISODate(today),
            events: deadlines[iso] ?? [],
        });
    }
    return cells;
});

function priorityColor(priority) {
    return { low: "success", medium: "warning", high: "error" }[priority] ?? "default";
}
</script>

<style scoped>
.calendar-weekdays {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    padding: 8px 0;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 500;
    color: rgba(var(--v-theme-on-surface), 0.6);
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
}

.calendar-cell {
    min-height: 96px;
    padding: 6px;
    border-right: 1px solid rgba(var(--v-theme-on-surface), 0.08);
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.08);
}

.calendar-cell--muted {
    color: rgba(var(--v-theme-on-surface), 0.35);
}

.calendar-cell--today span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: rgb(var(--v-theme-primary));
    color: rgb(var(--v-theme-on-primary));
}

.calendar-events {
    margin-top: 4px;
}
</style>
