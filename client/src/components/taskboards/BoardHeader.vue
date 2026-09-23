<script setup>
/**
 * @typedef {Object} BoardHeaderProps
 * @property {string} [boardName]
 * @property {string} [boardDescription]
 * @property {string} [icon]
 * @property {string} [visibility]
 */

/**
 * @type {BoardHeaderProps}
 */
const props = defineProps({
    boardName: {
        type: String,
        default: "Your taskboard",
    },
    boardDescription: {
        type: String,
        default: "Plan, prioritize, and track work across the project.",
    },
    icon: {
        type: String,
        default: "mdi-view-dashboard-outline",
    },
    visibility: {
        type: String,
        default: "Private",
    },
});

const emit = defineEmits(["action"]);

/**
 * @param {string} action
 */
function handleAction(action) {
    emit("action", action);
}
</script>

<template>
    <header class="board-header">
        <div class="board-header__identity">
            <div class="board-header__identity-content">
                <div class="board-header__title-row">
                    <h1 class="board-header__title">
                        {{ props.boardName }}
                    </h1>

                    <span class="board-header__visibility">
                        {{ props.visibility }}
                    </span>
                </div>

                <p class="board-header__description">
                    {{ props.boardDescription }}
                </p>
            </div>
        </div>

        <div class="board-header__actions">
            <button
                v-ripple
                type="button"
                class="board-header__icon-button"
                aria-label="Share board"
                @click="handleAction('share')"
            >
                <v-icon size="1.125rem"> mdi-share-variant-outline </v-icon>
            </button>

            <button
                v-ripple
                type="button"
                class="board-header__icon-button"
                aria-label="Board settings"
                @click="handleAction('settings')"
            >
                <v-icon size="1.125rem"> mdi-cog-outline </v-icon>
            </button>

            <v-btn
                color="primary"
                prepend-icon="mdi-account-plus-outline"
                variant="flat"
                density="comfortable"
                class="text-none board-toolbar__invite"
                @click="handleAction('invite')"
            >
                Invite people
            </v-btn>
        </div>
    </header>
</template>

<style scoped>
.board-header {
    flex: 0 0 auto;
    min-height: 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
}

.board-header__identity {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.625rem;
}

.board-header__icon {
    flex: 0 0 auto;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0.0625rem solid var(--v-theme-outline, #e1e4e8);
    border-radius: 0.375rem;
    background: var(--v-theme-surface-variant, #f8f9fa);
    color: var(--v-theme-text-secondary, #475467);
}

.board-header__identity-content {
    min-width: 0;
}

.board-header__title-row {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.board-header__title {
    margin: 0;
    overflow: hidden;
    color: var(--v-theme-on-surface, #1a1f2c);
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.board-header__visibility {
    flex: 0 0 auto;
    padding: 0.125rem 0.375rem;
    border: 0.0625rem solid var(--v-theme-outline-variant, #eaecf0);
    border-radius: 0.125rem;
    color: var(--v-theme-text-secondary, #475467);
    font-size: 0.6875rem;
    font-weight: 700;
    line-height: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    user-select: none;
    -webkit-user-select: none;
}

.board-header__description {
    margin: 0.125rem 0 0;
    overflow: hidden;
    color: var(--v-theme-text-secondary, #475467);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.board-header__actions {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.board-header__icon-button {
    width: 2rem;
    height: 2rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    border: 0.0625rem solid transparent;
    border-radius: 0.375rem;
    background: transparent;
    color: var(--v-theme-text-secondary, #475467);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    isolation: isolate;
    transition: color 0.15s ease;
}

.board-header__icon-button:hover {
    color: rgb(var(--v-theme-primary));
}

.board-header__icon-button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

.board-toolbar__invite {
    flex: 0 0 auto;
    border-radius: 0.5rem;
}

.board-toolbar__invite :deep(.v-btn__content) {
    user-select: none;
}
</style>
