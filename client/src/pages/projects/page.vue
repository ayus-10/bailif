<template>
    <v-container fluid class="pa-6">
        <!-- Header -->
        <div class="d-flex align-center mb-2">
            <v-icon :icon="project.icon" size="28" class="mr-3" />
            <div>
                <h1 class="text-h5 font-weight-medium">{{ project.name }}</h1>
                <span class="text-body-2 text-medium-emphasis">{{
                    project.description
                }}</span>
            </div>
            <v-spacer />
            <v-btn variant="outlined" prepend-icon="mdi-pencil-outline"
                >Edit</v-btn
            >
        </div>

        <v-row class="align-center mt-4 mb-2">
            <v-col cols="12" sm="6">
                <div class="d-flex justify-space-between text-caption mb-1">
                    <span>Progress</span>
                    <span>{{ project.progress }}%</span>
                </div>
                <v-progress-linear
                    :model-value="project.progress"
                    color="primary"
                    height="8"
                    rounded
                />
            </v-col>
            <v-col cols="12" sm="6" class="d-flex justify-sm-end">
                <v-avatar-group>
                    <v-avatar
                        v-for="member in project.members"
                        :key="member.id"
                        color="primary"
                        size="32"
                    >
                        <span class="text-caption">{{ member.initials }}</span>
                    </v-avatar>
                </v-avatar-group>
            </v-col>
        </v-row>

        <v-tabs v-model="tab" class="mt-4">
            <v-tab value="tasks">Tasks</v-tab>
            <v-tab value="files">Files</v-tab>
            <v-tab value="team">Team</v-tab>
        </v-tabs>
        <v-divider />

        <v-window v-model="tab" class="mt-4">
            <!-- Tasks -->
            <v-window-item value="tasks">
                <v-list lines="two">
                    <v-list-item v-for="task in project.tasks" :key="task.id">
                        <template #prepend>
                            <v-checkbox-btn
                                :model-value="task.status === 'done'"
                            />
                        </template>
                        <v-list-item-title>{{ task.title }}</v-list-item-title>
                        <v-list-item-subtitle
                            >Due {{ task.due }}</v-list-item-subtitle
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
            </v-window-item>

            <!-- Files -->
            <v-window-item value="files">
                <v-list>
                    <v-list-item
                        v-for="file in project.files"
                        :key="file.id"
                        :prepend-icon="fileIcon(file.type)"
                    >
                        <v-list-item-title>{{ file.name }}</v-list-item-title>
                        <v-list-item-subtitle
                            >{{ file.size }} · edited
                            {{ file.updated }}</v-list-item-subtitle
                        >
                    </v-list-item>
                </v-list>
            </v-window-item>

            <!-- Team -->
            <v-window-item value="team">
                <v-list>
                    <v-list-item
                        v-for="member in project.members"
                        :key="member.id"
                    >
                        <template #prepend>
                            <v-avatar color="primary" size="36">
                                <span class="text-body-2">{{
                                    member.initials
                                }}</span>
                            </v-avatar>
                        </template>
                        <v-list-item-title>{{ member.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{
                            member.role
                        }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>
            </v-window-item>
        </v-window>
    </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
    id: {
        type: [String, Number],
        default: null,
    },
});

const tab = ref("tasks");

// Mock project store, keyed by id. Swap for a real API/Pinia lookup.
const projectsById = {
    1: {
        id: 1,
        name: "Website Redesign",
        icon: "mdi-web",
        description: "Refresh the marketing site with the new brand system.",
        progress: 67,
        members: [
            { id: 1, name: "Maya Chen", initials: "MC", role: "Lead Designer" },
            {
                id: 2,
                name: "Devon Ray",
                initials: "DR",
                role: "Frontend Engineer",
            },
        ],
        tasks: [
            {
                id: 1,
                title: "Finalize homepage wireframes",
                due: "Today",
                priority: "high",
                status: "todo",
            },
            {
                id: 2,
                title: "Build component library",
                due: "Jul 30",
                priority: "medium",
                status: "in-progress",
            },
            {
                id: 3,
                title: "QA pass on staging",
                due: "Aug 2",
                priority: "low",
                status: "todo",
            },
        ],
        files: [
            {
                id: 1,
                name: "Wireframes-v3.fig",
                type: "design",
                size: "4.2 MB",
                updated: "2 days ago",
            },
            {
                id: 2,
                name: "Brand-guidelines.pdf",
                type: "pdf",
                size: "1.1 MB",
                updated: "1 week ago",
            },
        ],
    },
    2: {
        id: 2,
        name: "Mobile App",
        icon: "mdi-cellphone",
        description: "Native iOS/Android companion app.",
        progress: 25,
        members: [
            {
                id: 3,
                name: "Priya Nair",
                initials: "PN",
                role: "Product Manager",
            },
        ],
        tasks: [
            {
                id: 4,
                title: "Review API contract",
                due: "Tomorrow",
                priority: "medium",
                status: "todo",
            },
        ],
        files: [],
    },
};

const project = computed(
    () =>
        projectsById[props.id] ?? {
            id: props.id,
            name: "Untitled Project",
            icon: "mdi-folder-outline",
            description: "",
            progress: 0,
            members: [],
            tasks: [],
            files: [],
        },
);

function priorityColor(priority) {
    return (
        { low: "success", medium: "warning", high: "error" }[priority] ??
        "default"
    );
}

function fileIcon(type) {
    return (
        { design: "mdi-palette-outline", pdf: "mdi-file-pdf-box" }[type] ??
        "mdi-file-outline"
    );
}
</script>
