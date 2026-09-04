import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {
        path: "/",
        redirect: {
            name: "onboarding",
        },
    },

    {
        path: "/onboarding",
        redirect: { name: "project" },
        component: () => import("@/views/Onboarding.vue"),
        children: [
            {
                path: "project",
                name: "project",
                component: () =>
                    import("@/components/onboarding/NewProject.vue"),
            },
            {
                path: "taskboard",
                name: "taskboard",
                component: () =>
                    import("@/components/onboarding/NewTaskboard.vue"),
            },
        ],
    },

    {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("@/views/Dashboard.vue"),
        children: [
            {
                path: "overview",
                name: "overview",
                component: () => import("@/views/OverviewPage.vue"),
                props: true,
            },
            {
                path: "projects",
                name: "projects",
                component: () => import("@/views/ProjectDetail.vue"),
                props: true,
            },
            {
                path: "taskboards/all",
                name: "taskboards-all",
                component: () => import("@/views/TaskBoard.vue"),
            },
            {
                path: "taskboards/:id",
                name: "taskboards",
                component: () => import("@/views/TaskBoard.vue"),
            },
            {
                path: "tasks/:id",
                name: "task",
                component: () => import("@/views/TaskPage.vue"),
            },
            {
                path: "calendar",
                name: "calendar",
                component: () => import("@/views/Calendar.vue"),
            },
            {
                path: "documents",
                name: "documents",
                component: () => import("@/views/Documents.vue"),
            },
            {
                path: "gantt",
                name: "gantt",
                component: () => import("@/views/Gantt.vue"),
            },
            {
                path: "notifications",
                name: "notifications",
                component: () => import("@/views/Notifications.vue"),
            },
            {
                path: "settings",
                name: "settings",
                component: () => import("@/views/Settings.vue"),
            },
        ],
    },

    {
        path: "/:pathMatch(.*)*",
        redirect: {
            name: "dashboard",
        },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
