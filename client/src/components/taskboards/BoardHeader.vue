<script setup>
const props = defineProps({
    boardName: {
        type: String,
        default: "Your taskboard",
    },
    boardDescription: {
        type: String,
        default: "Plan, prioritize, and track work across the project.",
    },
    editable: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["edit", "delete"]);
</script>

<template>
    <header class="board-header">
        <div class="board-header__identity">
            <div class="board-header__identity-content">
                <div class="board-header__title-row">
                    <h1 class="board-header__title">
                        {{ props.boardName }}
                    </h1>
                </div>

                <p class="board-header__description">
                    {{ props.boardDescription }}
                </p>
            </div>
        </div>

        <div v-if="editable" class="board-header__actions">
            <button
                v-ripple
                type="button"
                class="board-header__icon-button"
                aria-label="Edit board"
                @click="emit('edit')"
            >
                <v-icon size="1.125rem"> mdi-pencil-outline </v-icon>
            </button>

            <button
                v-ripple
                type="button"
                class="board-header__icon-button"
                aria-label="Delete board"
                @click="emit('delete')"
            >
                <v-icon size="1.125rem"> mdi-delete-outline </v-icon>
            </button>
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
</style>
