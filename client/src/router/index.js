import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("../components/Dashboard.vue"),
  },
  {
    path: "/projects/:id?",
    name: "projects",
    component: () => import("../components/ProjectDetail.vue"),
    props: true,
  },
  {
    path: "/tasks",
    name: "tasks",
    component: () => import("../components/TaskBoard.vue"),
  },
  {
    path: "/calendar",
    name: "calendar",
    component: () => import("../components/CalendarView.vue"),
  },
  {
    path: "/documents",
    name: "documents",
    component: () => import("../components/DocumentSection.vue"),
  },
  {
    path: "/gantt",
    name: "gantt",
    component: () => import("../components/GanttChart.vue"),
  },
  {
    path: "/notifications",
    name: "notifications",
    component: () => import("../components/Notifications.vue"),
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("../components/Settings.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
