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
        name: "onboarding",
        component: () => import("@/views/Onboarding.vue"),
    },

    {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("@/views/Dashboard.vue"),
    },

    {
        path: "/projects/:id",
        name: "projects",
        component: () => import("@/views/ProjectDetail.vue"),
        props: true,
    },

    {
        path: "/tasks",
        name: "tasks",
        component: () => import("@/views/TaskBoard.vue"),
    },

    {
        path: "/tasks/:id",
        name: "task",
        component: () => import("@/views/TaskPage.vue"),
    },

    {
        path: "/calendar",
        name: "calendar",
        component: () => import("@/views/Calendar.vue"),
    },

    {
        path: "/documents",
        name: "documents",
        component: () => import("@/views/Documents.vue"),
    },

    {
        path: "/gantt",
        name: "gantt",
        component: () => import("@/views/Gantt.vue"),
    },

    {
        path: "/notifications",
        name: "notifications",
        component: () => import("@/views/Notifications.vue"),
    },

    {
        path: "/settings",
        name: "settings",
        component: () => import("@/views/Settings.vue"),
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
