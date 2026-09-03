<script setup lang="ts">
import { onMounted } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import { useTaskboardsStore } from "@/stores/taskboard.store";

const taskboardsStore = useTaskboardsStore();

onMounted(() => {
    const projectId = localStorage.getItem("project_id");
    if (projectId) taskboardsStore.fetch({ projectId });
});
</script>

<template>
    <aside>
        <Sidebar :task-boards="taskboardsStore.items" />
    </aside>
    <main class="main-content">
        <router-view />
    </main>
</template>
