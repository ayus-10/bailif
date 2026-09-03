<script setup>
import { onMounted, onUnmounted } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";

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

<template>
    <v-app>
        <Sidebar />

        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>
