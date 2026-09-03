<script setup lang="ts">
import Sidebar from "@/components/layout/Sidebar.vue";
</script>

<template>
    <aside>
        <Sidebar :task-boards="[]" />
    </aside>
    <main class="main-content">
        <router-view />
    </main>
</template>
