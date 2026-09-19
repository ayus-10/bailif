<script setup lang="ts">
import { onMounted, ref } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import CreateTaskBoardModel from "@/components/taskboards/CreateTaskBoardModel.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useTaskboardsStore } from "@/stores/taskboards.store";

// TODO: implement error boundary
const { projectId } = useActiveProject();

const taskboardsStore = useTaskboardsStore();

const showTaskboardModal = ref(false);

onMounted(() => {
    taskboardsStore.fetch({ projectPublicId: projectId.value });
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
            :project-id="projectId"
            @close="closeTaskboardModal"
        />
    </aside>

    <main class="main-content">
        <router-view />
    </main>
</template>
