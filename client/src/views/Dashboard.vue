<script setup lang="ts">
import { ref, watch } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import CreateTaskBoardModel from "@/components/taskboards/CreateTaskBoardModel.vue";
import { useActiveProject } from "@/composables/useActiveProject";
import { useToast } from "@/composables/useToast";
import { useTaskboardsStore } from "@/stores/taskboards.store";
import { showApiError } from "@/utils/errorHandlers";

const { projectId } = useActiveProject();

const taskboardsStore = useTaskboardsStore();
const toast = useToast();

const showTaskboardModal = ref(false);
const isRail = ref(false);

watch(
    projectId,
    (id) => {
        if (id) {
            taskboardsStore
                .fetch({ projectPublicId: id })
                .catch((err) => showApiError(err, toast));
        }
    },
    { immediate: true }
);

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
            :task-boards="taskboardsStore.items"
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
