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
import Sidebar from "./components/layout/Sidebar.vue";
import CommandDialog from "./components/layout/CommandDialog.vue";
</script>
