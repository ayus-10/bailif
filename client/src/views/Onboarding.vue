<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { computed } from "vue";
import TopProgressBar from "@/components/common/TopProgressBar.vue";
import NewProject from "@/components/onboarding/NewProject.vue";
import NewTaskboard from "@/components/onboarding/NewTaskboard.vue";

const route = useRoute();
const router = useRouter();

const steps = [
    {
        name: "new-project",
        component: NewProject,
        skippable: false,
    },
    {
        name: "new-taskboard",
        component: NewTaskboard,
        skippable: true,
    },
];

const currentStep = computed(() => {
    const index = steps.findIndex((step) => step.name === route.name);

    return index === -1 ? 1 : index + 1;
});

const currentStepConfig = computed(() => {
    return steps[currentStep.value - 1];
});

function handleSkip() {
    const nextStep = steps[currentStep.value];

    if (!nextStep) return;

    router.push({
        name: nextStep.name,
    });
}
</script>

<template>
    <div class="onboarding">
        <TopProgressBar
            :current-step="currentStep"
            :total-steps="steps.length"
            :can-skip="currentStepConfig.skippable"
            @skip="handleSkip"
        />

        <main class="onboarding-content">
            <RouterView />
        </main>
    </div>
</template>

<style scoped>
.onboarding {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.onboarding-content {
    flex: 1;
    width: 100%;
    background-color: #f4f5f7;
}
</style>
