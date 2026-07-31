<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Task Board</h1>
                <span class="text-body-2 text-medium-emphasis">
                    {{ filteredTasks.length }} task{{
                        filteredTasks.length === 1 ? "" : "s"
                    }}
                    <span v-if="route.query.status || route.query.priority"
                        >matching filters</span
                    >
                </span>
            </div>
            <v-spacer />
            <v-btn color="primary" prepend-icon="mdi-plus" variant="flat"
                >New Task</v-btn
            >
        </div>

        <!-- Active filter chips, clearable -->
        <div v-if="route.query.status || route.query.priority" class="mb-4">
            <v-chip
                v-if="route.query.status"
                closable
                size="small"
                class="mr-2"
                @click:close="clearFilter('status')"
            >
                Status: {{ route.query.status }}
            </v-chip>
            <v-chip
                v-if="route.query.priority"
                closable
                size="small"
                @click:close="clearFilter('priority')"
            >
                Priority: {{ route.query.priority }}
            </v-chip>
        </div>

        <v-row>
            <v-col
                v-for="column in columns"
                :key="column.status"
                cols="12"
                md="4"
            >
                <div class="d-flex align-center mb-2">
                    <v-icon :icon="column.icon" size="18" class="mr-2" />
                    <span class="text-subtitle-2 font-weight-medium">{{
                        column.label
                    }}</span>
                    <v-chip size="x-small" class="ml-2">{{
                        tasksFor(column.status).length
                    }}</v-chip>
                </div>

                <v-card
                    v-for="task in tasksFor(column.status)"
                    :key="task.id"
                    variant="outlined"
                    class="mb-3 pa-3"
                >
                    <div class="d-flex justify-space-between align-start">
                        <span class="text-body-2 font-weight-medium">{{
                            task.title
                        }}</span>
                        <v-chip
                            :color="priorityColor(task.priority)"
                            size="x-small"
                            variant="tonal"
                        >
                            {{ task.priority }}
                        </v-chip>
                    </div>
                    <div
                        class="text-caption text-medium-emphasis mt-2 d-flex align-center"
                    >
                        <v-icon
                            icon="mdi-folder-outline"
                            size="14"
                            class="mr-1"
                        />
                        {{ task.project }}
                        <v-spacer />
                        <v-icon
                            icon="mdi-calendar-blank-outline"
                            size="14"
                            class="mr-1"
                        />
                        {{ task.due }}
                    </div>
                </v-card>

                <v-sheet
                    v-if="tasksFor(column.status).length === 0"
                    class="pa-4 text-center text-caption text-medium-emphasis"
                    border
                    rounded
                >
                    No tasks here
                </v-sheet>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const columns = [
    { status: "todo", label: "To Do", icon: "mdi-circle-outline" },
    { status: "in-progress", label: "In Progress", icon: "mdi-progress-clock" },
    { status: "done", label: "Done", icon: "mdi-check-circle-outline" },
];

const tasks = [
    {
        id: 1,
        title: "Finalize homepage wireframes",
        project: "Website Redesign",
        due: "Today",
        priority: "high",
        status: "todo",
    },
    {
        id: 2,
        title: "Review API contract",
        project: "Mobile App",
        due: "Tomorrow",
        priority: "medium",
        status: "todo",
    },
    {
        id: 3,
        title: "Approve campaign copy",
        project: "Marketing Campaign",
        due: "Jul 28",
        priority: "low",
        status: "todo",
    },
    {
        id: 4,
        title: "Build component library",
        project: "Website Redesign",
        due: "Jul 30",
        priority: "medium",
        status: "in-progress",
    },
    {
        id: 5,
        title: "Wire up auth flow",
        project: "Mobile App",
        due: "Aug 1",
        priority: "high",
        status: "in-progress",
    },
    {
        id: 6,
        title: "Set up staging environment",
        project: "Mobile App",
        due: "Jul 29",
        priority: "medium",
        status: "done",
    },
    {
        id: 7,
        title: "QA pass on staging",
        project: "Website Redesign",
        due: "Aug 2",
        priority: "low",
        status: "done",
    },
];

const filteredTasks = computed(() =>
    tasks.filter((task) => {
        if (route.query.status && task.status !== route.query.status)
            return false;
        if (route.query.priority && task.priority !== route.query.priority)
            return false;
        return true;
    }),
);

function tasksFor(status) {
    return filteredTasks.value.filter((task) => task.status === status);
}

function priorityColor(priority) {
    return (
        { low: "success", medium: "warning", high: "error" }[priority] ??
        "default"
    );
}

function clearFilter(key) {
    const query = { ...route.query };
    delete query[key];
    router.push({ path: "/tasks", query });
}
</script>
