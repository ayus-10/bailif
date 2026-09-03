<script setup lang="ts">
import { onMounted, ref } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import CreateTaskBoardModel from "@/components/taskboards/CreateTaskBoardModel.vue";
import { useTaskboardsStore } from "@/stores/taskboard.store";

const taskboardsStore = useTaskboardsStore();

const showTaskboardModal = ref(false);

onMounted(() => {
    const projectId = localStorage.getItem("project_id");
    if (projectId) taskboardsStore.fetch({ projectId });
});

function openTaskboardModal() {
    showTaskboardModal.value = true;
}

function closeTaskboardModal() {
    showTaskboardModal.value = false;
}
</script>

<template>
    <aside>
        <Sidebar
            :task-boards="taskboardsStore.items"
            @new-board="openTaskboardModal"
        />

        <CreateTaskBoardModel
            :model-value="showTaskboardModal"
            @close="closeTaskboardModal"
        />
    </aside>

    <main class="main-content">
        <router-view />
    </main>
</template>
