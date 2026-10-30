<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import CreateTaskBoardModel from "@/components/taskboards/CreateTaskBoardModel.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useTaskboardsList } from "@/queries/taskboards.queries";

const { projectId } = useActiveProject();

const { items: taskBoards } = useTaskboardsList(projectId);

const showTaskboardModal = ref(false);
const isRail = ref(false);

function openTaskboardModal() {
    showTaskboardModal.value = true;
}

function closeTaskboardModal() {
    showTaskboardModal.value = false;
}
</script>

<template>
    <aside v-if="projectId">
        <Sidebar
            :task-boards="taskBoards"
            :rail="isRail"
            @toggle-rail="isRail = !isRail"
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
