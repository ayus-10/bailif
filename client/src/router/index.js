import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../pages/dashboard/page.vue"),
  },
  {
    path: "/projects/:id?",
    name: "projects",
    component: () => import("../pages/projects/page.vue"),
    props: true,
  },
  {
    path: "/tasks",
    name: "tasks",
    component: () => import("../pages/tasks/page.vue"),
  },
  {
    path: "/calendar",
    name: "calendar",
    component: () => import("../pages/calendar/page.vue"),
  },
  {
    path: "/documents",
    name: "documents",
    component: () => import("../pages/documents/page.vue"),
  },
  {
    path: "/gantt",
    name: "gantt",
    component: () => import("../pages/gantt/page.vue"),
  },
  {
    path: "/notifications",
    name: "notifications",
    component: () => import("../pages/notifications/page.vue"),
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("../pages/settings/page.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
