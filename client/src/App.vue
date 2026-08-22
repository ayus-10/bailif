<template>
    <v-app>
        <Sidebar @create-board="showCreateBoard = true" />

        <v-main>
            <router-view />

            <CommandDialog />

            <CreateTaskBoardModal
                v-model="showCreateBoard"
                @submit="createBoard"
            />
        </v-main>
    </v-app>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import CommandDialog from "./components/layout/CommandDialog.vue";
import Sidebar from "./components/layout/Sidebar.vue";
import CreateTaskBoardModal from "./components/tasks/CreateTaskBoardModal.vue";

const showCreateBoard = ref(false);

function createBoard(boardData) {
    // Create the board here.
    // e.g. store.dispatch("boards/create", boardData)
}

/** @param {MouseEvent} event */
function preventContextMenu(event) {
    event.preventDefault();
}

onMounted(() => {
    window.addEventListener("contextmenu", preventContextMenu);
});

onUnmounted(() => {
    window.removeEventListener("contextmenu", preventContextMenu);
});
</script>
