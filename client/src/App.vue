<template>
    <v-app>
        <Sidebar />
        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script setup>
import Sidebar from "./shared/layout/Sidebar.vue";
</script>
