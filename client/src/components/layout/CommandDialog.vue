<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";

import { chat, searchTasks, suggestTasks } from "@/api/ai-actions.api";

const open = ref(false);

const mode = ref("chat");
const projectId = ref("");
const prompt = ref("");

const loading = ref(false);
const response = ref(null);
const error = ref(null);

const canSubmit = computed(() => {
    return prompt.value.trim().length > 0;
});

async function submit() {
    loading.value = true;
    error.value = null;
    response.value = null;

    try {
        const payload = {
            message: prompt.value,
            query: prompt.value,
            title: prompt.value,
            project_id: projectId.value || null,
        };

        if (mode.value === "chat") {
            response.value = await chat(payload);
        } else if (mode.value === "search_tasks") {
            response.value = await searchTasks(payload);
        } else {
            response.value = await suggestTasks(payload);
        }
    } catch (e) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
}

function onKeydown(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        open.value = !open.value;
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

                <v-chip size="small"> Ctrl + K </v-chip>
            </v-card-title>

            <v-card-text>
                <v-select
                    v-model="mode"
                    label="Mode"
                    :items="[
                        {
                            title: 'Chat',
                            value: 'chat',
                        },
                        {
                            title: 'Search tasks',
                            value: 'search_tasks',
                        },
                        {
                            title: 'Suggest tasks',
                            value: 'suggest_tasks',
                        },
                    ]"
                />

                <v-text-field
                    v-model="projectId"
                    label="Project ID (optional)"
                />

                <v-textarea
                    v-model="prompt"
                    label="Ask anything..."
                    rows="4"
                    autofocus
                    @keydown.enter.ctrl.prevent="submit"
                />

                <v-alert v-if="error" type="error" class="mt-4">
                    {{ error }}
                </v-alert>

                <template v-if="response">
                    <v-divider class="my-4" />

                    <div class="text-h6 mb-2">Reply</div>

                    <p>{{ response.reply }}</p>

                    <div v-if="response.actions.length" class="mt-4">
                        <div class="text-h6 mb-2">Actions</div>

                        <v-card
                            v-for="(action, i) in response.actions"
                            :key="i"
                            class="mb-2"
                            variant="outlined"
                        >
                            <v-card-title>
                                {{ action.type }}
                            </v-card-title>

                            <v-card-text>
                                <pre>{{
                                    JSON.stringify(action.data, null, 2)
                                }}</pre>
                            </v-card-text>
                        </v-card>
                    </div>

                    <div v-if="response.results" class="mt-4">
                        <div class="text-h6 mb-2">Results</div>

                        <pre>{{
                            JSON.stringify(response.results, null, 2)
                        }}</pre>
                    </div>
                </template>
            </v-card-text>

            <v-card-actions>
                <v-spacer />

                <v-btn variant="text" @click="open = false"> Close </v-btn>

                <v-btn
                    color="primary"
                    :loading="loading"
                    :disabled="!canSubmit"
                    @click="submit"
                >
                    Send
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
