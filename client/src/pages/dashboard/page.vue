<template>
    <v-container fluid class="pa-6">
        <!-- Page header -->
        <div class="d-flex align-center mb-6">
            <div>
                <h1 class="text-h5 font-weight-medium">Dashboard</h1>
                <span class="text-body-2 text-medium-emphasis">
                    Here's what's happening across your projects
                </span>
            </div>
            <v-spacer />
            <v-btn color="primary" prepend-icon="mdi-plus" variant="flat">
                New Task
            </v-btn>
        </div>

        <!-- Metrics -->
        <v-row>
            <v-col
                v-for="metric in metrics"
                :key="metric.label"
                cols="12"
                sm="6"
                md="3"
            >
                <v-card variant="outlined" class="pa-4">
                    <div class="d-flex align-center justify-space-between">
                        <span class="text-body-2 text-medium-emphasis">{{
                            metric.label
                        }}</span>
                        <v-icon
                            :color="metric.color"
                            :icon="metric.icon"
                            size="20"
                        />
                    </div>
                    <div class="text-h4 font-weight-medium mt-2">
                        {{ metric.value }}
                    </div>
                    <div class="text-caption text-medium-emphasis mt-1">
                        {{ metric.hint }}
                    </div>
                </v-card>
            </v-col>
        </v-row>

        <v-row class="mt-2">
            <!-- Project progress -->
            <v-col cols="12" md="7">
                <v-card variant="outlined">
                    <v-card-item>
                        <v-card-title
                            class="text-subtitle-1 font-weight-medium"
                        >
                            Active Projects
                        </v-card-title>
                    </v-card-item>
                    <v-divider />
                    <v-list lines="two">
                        <v-list-item
                            v-for="project in projects"
                            :key="project.id"
                        >
                            <template #prepend>
                                <v-icon :icon="project.icon" class="mr-2" />
                            </template>

                            <v-list-item-title class="font-weight-medium">
                                {{ project.name }}
                            </v-list-item-title>
                            <v-list-item-subtitle>
                                {{ project.tasksDone }} /
                                {{ project.tasksTotal }} tasks complete
                            </v-list-item-subtitle>

                            <template #append>
                                <div style="width: 140px">
                                    <div
                                        class="d-flex justify-space-between text-caption mb-1"
                                    >
                                        <span>{{ project.progress }}%</span>
                                    </div>
                                    <v-progress-linear
                                        :model-value="project.progress"
                                        :color="progressColor(project.progress)"
                                        height="6"
                                        rounded
                                    />
                                </div>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>

            <!-- Upcoming / recent tasks -->
            <v-col cols="12" md="5">
                <v-card variant="outlined">
                    <v-card-item>
                        <v-card-title
                            class="text-subtitle-1 font-weight-medium"
                        >
                            Upcoming Tasks
                        </v-card-title>
                    </v-card-item>
                    <v-divider />
                    <v-list>
                        <v-list-item
                            v-for="task in upcomingTasks"
                            :key="task.id"
                        >
                            <template #prepend>
                                <v-checkbox-btn
                                    :model-value="task.status === 'done'"
                                />
                            </template>

                            <v-list-item-title>{{
                                task.title
                            }}</v-list-item-title>
                            <v-list-item-subtitle
                                >{{ task.project }} · due
                                {{ task.due }}</v-list-item-subtitle
                            >

                            <template #append>
                                <v-chip
                                    :color="priorityColor(task.priority)"
                                    size="small"
                                    variant="tonal"
                                >
                                    {{ task.priority }}
                                </v-chip>
                            </template>
                        </v-list-item>
                    </v-list>
                    <v-divider />
                    <v-card-actions>
                        <v-spacer />
                        <v-btn
                            variant="text"
                            size="small"
                            append-icon="mdi-arrow-right"
                        >
                            View all tasks
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <!-- Recent activity -->
                <v-card variant="outlined" class="mt-4">
                    <v-card-item>
                        <v-card-title
                            class="text-subtitle-1 font-weight-medium"
                        >
                            Recent Activity
                        </v-card-title>
                    </v-card-item>
                    <v-divider />
                    <v-list density="compact">
                        <v-list-item
                            v-for="activity in recentActivity"
                            :key="activity.id"
                        >
                            <template #prepend>
                                <v-avatar color="primary" size="28">
                                    <span class="text-caption">{{
                                        activity.initials
                                    }}</span>
                                </v-avatar>
                            </template>
                            <v-list-item-title class="text-body-2">
                                <strong>{{ activity.actor }}</strong>
                                {{ activity.action }}
                            </v-list-item-title>
                            <v-list-item-subtitle class="text-caption">
                                {{ activity.time }}
                            </v-list-item-subtitle>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
/**
 * @typedef {Object} Metric
 * @property {string} label
 * @property {string|number} value
 * @property {string} hint
 * @property {string} icon
 * @property {string} color
 */

/** @type {Metric[]} */
const metrics = [
    {
        label: "Open Tasks",
        value: 24,
        hint: "6 due this week",
        icon: "mdi-checkbox-marked-outline",
        color: "primary",
    },
    {
        label: "Overdue",
        value: 3,
        hint: "Needs attention",
        icon: "mdi-alert-circle-outline",
        color: "error",
    },
    {
        label: "Active Projects",
        value: 5,
        hint: "2 nearing deadline",
        icon: "mdi-folder-multiple-outline",
        color: "info",
    },
    {
        label: "Completion Rate",
        value: "78%",
        hint: "Up 4% this month",
        icon: "mdi-trending-up",
        color: "success",
    },
];

const projects = [
    {
        id: 1,
        name: "Website Redesign",
        icon: "mdi-web",
        tasksDone: 12,
        tasksTotal: 18,
        progress: 67,
    },
    {
        id: 2,
        name: "Mobile App",
        icon: "mdi-cellphone",
        tasksDone: 5,
        tasksTotal: 20,
        progress: 25,
    },
    {
        id: 3,
        name: "Marketing Campaign",
        icon: "mdi-bullhorn-outline",
        tasksDone: 9,
        tasksTotal: 10,
        progress: 90,
    },
];

const upcomingTasks = [
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
        title: "Set up staging environment",
        project: "Mobile App",
        due: "Jul 29",
        priority: "medium",
        status: "done",
    },
];

const recentActivity = [
    {
        id: 1,
        actor: "Maya",
        initials: "M",
        action: "commented on Homepage wireframes",
        time: "10 min ago",
    },
    {
        id: 2,
        actor: "Devon",
        initials: "D",
        action: "completed Set up staging environment",
        time: "1 hr ago",
    },
    {
        id: 3,
        actor: "Priya",
        initials: "P",
        action: "created Approve campaign copy",
        time: "3 hr ago",
    },
];

function priorityColor(priority) {
    return (
        { low: "success", medium: "warning", high: "error" }[priority] ??
        "default"
    );
}

function progressColor(value) {
    if (value >= 75) return "success";
    if (value >= 40) return "info";
    return "warning";
}
</script>
