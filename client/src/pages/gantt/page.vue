<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Gantt Chart</h1>
                <span class="text-body-2 text-medium-emphasis"
                    >{{ project.name }} schedule</span
                >
            </div>
            <v-spacer />
            <v-select
                v-model="selectedProjectId"
                :items="projectOptions"
                item-title="name"
                item-value="id"
                density="compact"
                variant="outlined"
                hide-details
                style="max-width: 240px"
            />
        </div>

        <v-card variant="outlined" class="pa-4">
            <div class="gantt-scroll">
                <div class="gantt-grid" :style="gridStyle">
                    <!-- Day header row -->
                    <div class="gantt-corner" />
                    <div
                        v-for="day in days"
                        :key="day.iso"
                        class="gantt-day-header text-caption text-center"
                        :class="{ 'gantt-day-header--weekend': day.isWeekend }"
                    >
                        {{ day.label }}
                    </div>

                    <!-- Task rows -->
                    <template
                        v-for="(task, rowIndex) in project.tasks"
                        :key="task.id"
                    >
                        <div class="gantt-row-label text-body-2">
                            {{ task.title }}
                        </div>
                        <div
                            class="gantt-bar-track"
                            :style="{
                                gridColumn: `2 / span ${days.length}`,
                                gridRow: rowIndex + 2,
                            }"
                        >
                            <div
                                class="gantt-bar"
                                :class="`gantt-bar--${task.priority}`"
                                :style="barStyle(task)"
                                :title="`${task.title}: ${task.start} → ${task.end}`"
                            >
                                {{ task.title }}
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div class="d-flex align-center mt-4">
                <span class="text-caption text-medium-emphasis mr-4"
                    >Priority:</span
                >
                <v-chip
                    color="error"
                    size="x-small"
                    variant="tonal"
                    class="mr-2"
                    >High</v-chip
                >
                <v-chip
                    color="warning"
                    size="x-small"
                    variant="tonal"
                    class="mr-2"
                    >Medium</v-chip
                >
                <v-chip color="success" size="x-small" variant="tonal"
                    >Low</v-chip
                >
            </div>
        </v-card>

        <!-- Dependency list, since arrows across a scrollable grid get messy -->
        <v-card variant="outlined" class="mt-4">
            <v-card-item>
                <v-card-title class="text-subtitle-1 font-weight-medium"
                    >Dependencies</v-card-title
                >
            </v-card-item>
            <v-divider />
            <v-list density="compact">
                <v-list-item
                    v-for="dep in dependencyList"
                    :key="`${dep.from}-${dep.to}`"
                    prepend-icon="mdi-arrow-right-thin"
                >
                    <v-list-item-title class="text-body-2">
                        {{ dep.fromTitle }}
                        <span class="text-medium-emphasis"
                            >must finish before</span
                        >
                        {{ dep.toTitle }}
                    </v-list-item-title>
                </v-list-item>
                <v-list-item v-if="dependencyList.length === 0">
                    <v-list-item-title class="text-body-2 text-medium-emphasis">
                        No dependencies for this project
                    </v-list-item-title>
                </v-list-item>
            </v-list>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const projects = [
    {
        id: 1,
        name: "Website Redesign",
        rangeStart: "2026-07-20",
        rangeEnd: "2026-08-10",
        tasks: [
            {
                id: 1,
                title: "Wireframes",
                start: "2026-07-20",
                end: "2026-07-25",
                priority: "high",
            },
            {
                id: 2,
                title: "Component library",
                start: "2026-07-24",
                end: "2026-07-31",
                priority: "medium",
                dependsOn: 1,
            },
            {
                id: 3,
                title: "QA pass",
                start: "2026-08-01",
                end: "2026-08-05",
                priority: "low",
                dependsOn: 2,
            },
        ],
    },
    {
        id: 2,
        name: "Mobile App",
        rangeStart: "2026-07-22",
        rangeEnd: "2026-08-12",
        tasks: [
            {
                id: 4,
                title: "API contract",
                start: "2026-07-22",
                end: "2026-07-27",
                priority: "medium",
            },
            {
                id: 5,
                title: "Auth flow",
                start: "2026-07-27",
                end: "2026-08-03",
                priority: "high",
                dependsOn: 4,
            },
            {
                id: 6,
                title: "Staging setup",
                start: "2026-07-25",
                end: "2026-07-29",
                priority: "medium",
            },
        ],
    },
];

const selectedProjectId = ref(projects[0].id);
const projectOptions = projects.map((p) => ({ id: p.id, name: p.name }));
const project = computed(() =>
    projects.find((p) => p.id === selectedProjectId.value),
);

function toDate(iso) {
    return new Date(`${iso}T00:00:00`);
}

const days = computed(() => {
    const start = toDate(project.value.rangeStart);
    const end = toDate(project.value.rangeEnd);
    const list = [];
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
        const iso = d.toISOString().slice(0, 10);
        list.push({
            iso,
            label: d.toLocaleDateString(undefined, {
                day: "numeric",
                month: "short",
            }),
            isWeekend: d.getDay() === 0 || d.getDay() === 6,
        });
    }
    return list;
});

const gridStyle = computed(() => ({
    gridTemplateColumns: `180px repeat(${days.value.length}, minmax(36px, 1fr))`,
}));

function dayIndex(iso) {
    return days.value.findIndex((d) => d.iso === iso);
}

function barStyle(task) {
    const startIdx = dayIndex(task.start);
    const endIdx = dayIndex(task.end);
    const span = Math.max(1, endIdx - startIdx + 1);
    return {
        gridColumnStart: startIdx + 1,
        gridColumnEnd: `span ${span}`,
    };
}

const dependencyList = computed(() =>
    project.value.tasks
        .filter((t) => t.dependsOn)
        .map((t) => ({
            from: t.dependsOn,
            to: t.id,
            fromTitle: project.value.tasks.find((p) => p.id === t.dependsOn)
                ?.title,
            toTitle: t.title,
        })),
);
</script>

<style scoped>
.gantt-scroll {
    overflow-x: auto;
}

.gantt-grid {
    display: grid;
    grid-auto-rows: 40px;
    align-items: center;
    min-width: 600px;
}

.gantt-corner {
    grid-row: 1;
    grid-column: 1;
}

.gantt-day-header {
    grid-row: 1;
    padding: 4px 0;
    border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.12);
    color: rgba(var(--v-theme-on-surface), 0.6);
}

.gantt-day-header--weekend {
    background: rgba(var(--v-theme-on-surface), 0.03);
}

.gantt-row-label {
    grid-column: 1;
    padding-right: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.gantt-bar-track {
    display: grid;
    grid-template-columns: subgrid;
    height: 28px;
}

.gantt-bar {
    height: 24px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    padding: 0 8px;
    font-size: 0.7rem;
    color: white;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.gantt-bar--high {
    background: rgb(var(--v-theme-error));
}

.gantt-bar--medium {
    background: rgb(var(--v-theme-warning));
}

.gantt-bar--low {
    background: rgb(var(--v-theme-success));
}
</style>
