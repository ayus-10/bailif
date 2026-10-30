<script setup>
import { useRoute, useRouter } from "vue-router";
import { onMounted, onUnmounted, watch } from "vue";
import ToastContainer from "./components/layout/ToastContainer.vue";
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();
const route = useRoute();
const router = useRouter();

watch(
    () => authStore.isAuthenticated,
    (isAuthenticated) => {
        if (!isAuthenticated && route.meta.requiresAuth) {
            router.replace({
                name: "login",
                query: { redirect: route.fullPath },
            });
        }
    }
);

/**
 * @param {MouseEvent} event
 */
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
        <v-main>
            <router-view />
            <ToastContainer />
        </v-main>
    </v-app>
</template>
