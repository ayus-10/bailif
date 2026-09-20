<template>
    <div class="project-empty-state">
        <div class="project-empty-state__visual">
            <img
                src="@/assets/sad-robot.svg"
                alt="Not found"
                aria-hidden="true"
                class="project-empty-state__robot"
            />
        </div>

        <div class="project-empty-state__copy">
            <h2 class="project-empty-state__title">No active project yet</h2>

            <p class="project-empty-state__description">
                Select an existing project or create a new one to get started.
            </p>

            <v-btn
                to="/dashboard/projects"
                color="primary"
                variant="flat"
                density="comfortable"
                class="project-empty-state__action text-none"
                v-ripple
            >
                Select or create a project
            </v-btn>
        </div>
    </div>
</template>

<style scoped>
.project-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 2rem;
}

.project-empty-state__visual {
    flex: 0 0 15rem;
    width: 15rem;
    height: 15rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.project-empty-state__robot {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.project-empty-state__copy {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 28rem;
}

.project-empty-state__title {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.4;
}

.project-empty-state__description {
    margin: 0.5rem 0 1.25rem;
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
    font-size: 0.8125rem;
    font-weight: 400;
    line-height: 1.5;
}

.project-empty-state__action {
    border-radius: 0.625rem;
    font-size: 0.8125rem;
    font-weight: 500;
    user-select: none;
    -webkit-user-select: none;
}

.project-empty-state__action:focus-visible {
    box-shadow: 0 0 0 0.1875rem rgba(25, 118, 210, 0.15);
}

@media (max-width: 37.5rem) {
    .project-empty-state {
        flex-direction: column;
        gap: 1rem;
        padding: 1.5rem 1rem;
        text-align: center;
    }

    .project-empty-state__visual {
        flex-basis: auto;
        width: 10rem;
        height: 10rem;
    }

    .project-empty-state__copy {
        max-width: 24rem;
    }
}
</style>
