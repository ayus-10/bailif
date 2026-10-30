import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";
import { VueQueryPlugin } from "@tanstack/vue-query";
import { queryClient } from "@/queries/client";
import { useAuthStore } from "./stores/auth";

const app = createApp(App);
const pinia = createPinia();
const vuetify = createVuetify({
    components,
    directives,
});

app.use(pinia);
app.use(vuetify);
app.use(VueQueryPlugin, { queryClient });

const authStore = useAuthStore();

async function bootstrap() {
    try {
        await authStore.initialize();
    } catch (err) {
        console.error("Auth initialization failed:", err);
    } finally {
        app.use(router);
        app.mount("#app");
    }
}

bootstrap();
