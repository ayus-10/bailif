import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
    {
        path: "/",
        redirect: {
            name: "onboarding",
        },
    },

    {
        path: "/login",
        name: "login",
        component: () => import("@/views/LoginPage.vue"),
        meta: { guestOnly: true },
    },

    {
        path: "/onboarding",
        name: "onboarding",
        redirect: { name: "project" },
        component: () => import("@/views/Onboarding.vue"),
        meta: { requiresAuth: true, isOnboardingRoute: true },
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
        meta: { requiresAuth: true },

        children: [
            {
                path: "overview",
                name: "overview",
                component: () => import("@/views/OverviewPage.vue"),
                props: true,
            },

            {
                path: "project",
                name: "project-list",
                component: () => import("@/views/ProjectList.vue"),
            },
            {
                path: "project/new",
                name: "project-new",
                component: () => import("@/views/CreateProject.vue"),
            },
            {
                path: "project/:id",
                name: "project-overview",
                component: () => import("@/views/ProjectOverview.vue"),
                props: true,
            },
            {
                path: "project/:id/settings",
                name: "project-settings",
                component: () => import("@/views/ProjectSettings.vue"),
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

router.beforeEach((to) => {
    const authStore = useAuthStore();

    const isAuthenticated = authStore.isAuthenticated;
    const isOnboardingComplete = authStore.isOnboardingComplete;

    if (to.meta.requiresAuth && !isAuthenticated) {
        return {
            name: "login",
            query: {
                redirect: to.fullPath,
            },
        };
    }

    if (to.meta.guestOnly && isAuthenticated) {
        return { name: "dashboard" };
    }

    if (to.meta.isOnboardingRoute && isAuthenticated && isOnboardingComplete) {
        return { name: "dashboard" };
    }

    if (
        to.meta.requiresAuth &&
        !to.meta.isOnboardingRoute &&
        isAuthenticated &&
        !isOnboardingComplete
    ) {
        return { name: "onboarding" };
    }

    return true;
});

export default router;
