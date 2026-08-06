<script setup>
import { ref } from "vue";
import { PRIORITY_COLORS } from "@/constants/tasks";

const emit = defineEmits(["submit"]);

const form = ref({
    title: "",
    description: "",
    priority: "medium",
    due_date: null,
    project_id: null,
});

const priorities = Object.keys(PRIORITY_COLORS);

function createTask() {
    emit("submit", { ...form.value });

    form.value = {
        title: "",
        description: "",
        priority: "medium",
        due_date: null,
        project_id: null,
    };
}
</script>

<template>
    <v-card variant="outlined" class="mb-3 pa-4">
        <div class="d-flex align-center mb-4">
            <v-icon icon="mdi-plus-circle-outline" class="mr-2" />

            <span class="text-body-1 font-weight-medium">
                Create new task
            </span>
        </div>

        <v-form @submit.prevent="createTask">
            <v-text-field
                v-model="form.title"
                label="Title"
                variant="outlined"
                density="comfortable"
                hide-details
                class="mb-3"
            />

            <v-textarea
                v-model="form.description"
                label="Description"
                variant="outlined"
                rows="3"
                auto-grow
                hide-details
                class="mb-3"
            />

            <div class="d-flex ga-3 mb-3">
                <v-select
                    v-model="form.priority"
                    :items="priorities"
                    label="Priority"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                >
                    <template #selection="{ item }">
                        <v-chip
                            :color="PRIORITY_COLORS[item.title]"
                            size="small"
                            variant="tonal"
                        >
                            {{ item.title }}
                        </v-chip>
                    </template>
                </v-select>

                <v-text-field
                    v-model="form.due_date"
                    type="date"
                    label="Due date"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                />
            </div>

            <v-btn type="submit" color="primary" block prepend-icon="mdi-plus">
                Create task
            </v-btn>
        </v-form>
    </v-card>
</template>
