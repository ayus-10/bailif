<script setup>
import { computed } from "vue";

const props = defineProps({
    currentStep: {
        type: Number,
        required: true,
    },
    totalSteps: {
        type: Number,
        required: true,
    },
    canSkip: {
        type: Boolean,
        default: false,
    },
    skipLabel: {
        type: String,
        default: "Skip",
    },
});

const emit = defineEmits(["skip"]);

const steps = computed(() =>
    Array.from({ length: props.totalSteps }, (_, index) => index + 1)
);

/** @param {number} step */
function getStepState(step) {
    if (step < props.currentStep) return "completed";
    if (step === props.currentStep) return "current";
    return "upcoming";
}
</script>

<template>
    <div class="top-progress-bar">
        <div class="progress-header">
            <div class="step-meta">
                <span class="step-count text-uppercase"
                    >Step {{ currentStep }} of {{ totalSteps }}</span
                >
            </div>

            <button
                v-if="canSkip"
                type="button"
                class="skip-btn"
                @click="emit('skip')"
            >
                {{ skipLabel }}
            </button>
        </div>

        <div
            class="segmented-track"
            role="progressbar"
            :aria-valuemin="1"
            :aria-valuemax="totalSteps"
            :aria-valuenow="currentStep"
        >
            <div
                v-for="step in steps"
                :key="step"
                class="track-segment"
                :class="`track-segment--${getStepState(step)}`"
            />
        </div>
    </div>
</template>

<style scoped>
.top-progress-bar {
    display: flex;
    flex-direction: column;
    padding: 0.5rem;
    width: 100%;
}

.progress-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.step-meta {
    display: flex;
    align-items: center;
}

.step-count {
    font-size: 0.6875rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--v-theme-accent, #1976d2);
}

.skip-btn {
    background: transparent;
    border: none;
    padding: 0;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--v-theme-on-surface-variant, #475467);
    cursor: pointer;
    transition: color 0.15s ease;
}

.skip-btn:hover {
    color: var(--v-theme-accent, #1976d2);
}

.skip-btn:focus-visible {
    outline: 0.125rem solid var(--v-theme-accent, #1976d2);
    outline-offset: 0.125rem;
    border-radius: 0.125rem;
}

.segmented-track {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    width: 100%;
    height: 0.25rem;
}

.track-segment {
    flex: 1;
    height: 100%;
    border-radius: 0.125rem;
    transition: background-color 0.2s ease;
}

.track-segment--completed {
    background-color: var(--v-theme-accent, #1976d2);
}

.track-segment--current {
    background-color: var(--v-theme-accent, #1976d2);
}

.track-segment--upcoming {
    background-color: var(--v-theme-outline-variant, #eaecf0);
}
</style>
