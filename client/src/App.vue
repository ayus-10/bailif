<template>
    <v-app>
        <Sidebar />
        <v-main>
            <router-view />

            <CommandDialog />
        </v-main>
    </v-app>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import CommandDialog from "./components/layout/CommandDialog.vue";
import Sidebar from "./components/layout/Sidebar.vue";

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
