<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { chat } from "@/api/ai-actions.api";

/** @type {import("vue").Ref<boolean>} */
const open = ref(false);

/** @type {import("vue").Ref<string>} */
const prompt = ref("");

/** @type {import("vue").Ref<boolean>} */
const loading = ref(false);

/** @type {import("vue").Ref<unknown>} */
const response = ref(null);

/** @type {import("vue").Ref<string|null>} */
const error = ref(null);

/**
 * @returns {Promise<void>}
 */
async function submit() {
    const message = prompt.value.trim();

    if (!message || loading.value) {
        return;
    }

    loading.value = true;
    error.value = null;
    response.value = null;

    try {
        response.value = await chat({
            message,
        });
    } catch (e) {
        error.value = e instanceof Error ? e.message : "Something went wrong.";
    } finally {
        loading.value = false;
    }
}

/**
 * @param {KeyboardEvent} e
 * @returns {void}
 */
function onKeydown(e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        open.value = !open.value;
        return;
    }

    if (e.key === "Escape") {
        open.value = false;
    }
}

onMounted(() => {
    window.addEventListener("keydown", onKeydown);
});

onUnmounted(() => {
    window.removeEventListener("keydown", onKeydown);
});
</script>

<template>
    <v-dialog v-model="open" max-width="800">
        <v-card>
            <v-card-title class="d-flex align-center">
                AI Assistant

                <v-spacer />

                <v-chip size="small">Ctrl + K</v-chip>
            </v-card-title>

            <v-card-text>
                <v-textarea
                    v-model="prompt"
                    label="Ask anything..."
                    rows="4"
                    autofocus
                    :disabled="loading"
                    @keydown.enter.ctrl.prevent="submit"
                    @keydown.enter.meta.prevent="submit"
                />

                <v-alert v-if="error" type="error" class="mt-4">
                    {{ error }}
                </v-alert>

                <template v-if="response">
                    <v-divider class="my-4" />

                    <pre class="text-body-2">{{
                        JSON.stringify(response, null, 2)
                    }}</pre>
                </template>
            </v-card-text>

            <v-card-actions>
                <v-spacer />

                <v-btn variant="text" @click="open = false"> Close </v-btn>

                <v-btn
                    color="primary"
                    :loading="loading"
                    :disabled="!prompt.trim()"
                    @click="submit"
                >
                    Send
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
