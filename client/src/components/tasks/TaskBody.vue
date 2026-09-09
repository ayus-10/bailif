<script setup>
import { QuillEditor } from "@vueup/vue-quill";
import { isHtmlEmpty } from "@/utils/htmlFormatters";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "@/components/quill-editor.css";
import { ref } from "vue";

/** @typedef {import("@/types/task").TaskRead} TaskRead */
/** @typedef {import("@/types/task").TaskDraft} TaskDraft */

const props = defineProps({
    task: {
        /** @type {import("vue").PropType<TaskRead>} */
        type: Object,
        required: true,
    },
    draft: {
        /** @type {import("vue").PropType<TaskDraft>} */
        type: Object,
        required: true,
    },
    isEditing: Boolean,
});

const emit = defineEmits(["edit", "cancel", "save"]);

const toolbarOptions = [
    ["bold", "italic", "underline"],
    [{ list: "ordered" }, { list: "bullet" }, { list: "check" }],
];

const quill = ref(null);

// @ts-ignore
function onEditorReady(quillInstance) {
    quill.value = quillInstance;
    if (props.isEditing) {
        quillInstance.focus();
    }
}
</script>

<template>
    <section class="panel">
        <div class="panel__heading">
            <h2 class="panel__label">
                {{ isEditing ? "Edit description" : "Description" }}
            </h2>

            <div v-if="isEditing" class="panel__actions">
                <v-btn
                    icon="mdi-close"
                    size="small"
                    variant="text"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Cancel title edit"
                    @click="emit('cancel')"
                />

                <v-btn
                    icon="mdi-check"
                    size="small"
                    color="primary"
                    variant="tonal"
                    density="comfortable"
                    rounded="pill"
                    aria-label="Save title"
                    @click="emit('save')"
                />
            </div>

            <v-btn
                v-else
                class="panel__edit-btn"
                icon="mdi-pencil-outline"
                size="x-small"
                variant="text"
                density="comfortable"
                aria-label="Edit description"
                @click="emit('edit')"
            />
        </div>

        <div
            v-if="isEditing"
            class="description-editor"
            tabindex="0"
            @keydown.esc.prevent="emit('cancel')"
        >
            <QuillEditor
                v-model:content="draft.description"
                content-type="html"
                theme="snow"
                placeholder="Add a description..."
                :toolbar="toolbarOptions"
                @ready="onEditorReady"
            />
        </div>

        <div
            v-else-if="!isHtmlEmpty(task.description)"
            class="prose"
            v-html="task.description"
            @click="emit('edit')"
        />

        <button v-else type="button" class="panel__empty" @click="emit('edit')">
            <v-icon icon="mdi-text-box-plus-outline" size="16" />
            <span>No description yet — click to add one</span>
        </button>
    </section>
</template>

<style scoped>
.panel {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    padding: 0.875rem 1rem;
    border-radius: 0.75rem;
    background: rgb(var(--v-theme-surface));
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
    transition: border-color 0.12s ease;
}

.panel:hover {
    border-color: rgb(var(--v-theme-outline, 225, 228, 232));
}

.panel__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    min-height: 1.5rem;
}

.panel__actions {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    flex-shrink: 0;
}

.panel__actions .v-btn {
    border-radius: 999px;
}

.description-editor:focus {
    outline: none;
}

.panel__label {
    margin: 0;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25rem;
}

.panel__edit-btn {
    opacity: 0;
    transition: opacity 0.12s ease;
}

.panel:hover .panel__edit-btn,
.panel:focus-within .panel__edit-btn {
    opacity: 1;
}

.panel__edit-btn:deep(.v-icon) {
    color: rgb(var(--v-theme-text-secondary, 71, 84, 103));
}

.panel__edit-btn:hover:deep(.v-icon) {
    color: #1976d2;
}

.panel__empty {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    width: 100%;
    padding: 0.75rem;
    border: 0.0625rem dashed rgb(var(--v-theme-outline-variant, 234, 236, 240));
    border-radius: 0.625rem;
    background: transparent;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    transition:
        border-color 0.12s ease,
        color 0.12s ease;
}

.panel__empty:hover {
    border-color: rgba(25, 118, 210, 0.35);
    color: #1976d2;
}

.prose {
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.8125rem;
    line-height: 1.5;
    cursor: pointer;
    border-radius: 0.5rem;
    margin: -0.25rem -0.375rem;
    padding: 0.25rem 0.375rem;
    transition: background-color 0.12s ease;
}

.prose:hover {
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
}

.prose:deep(p) {
    margin: 0 0 0.5rem;
}

.prose:deep(p:last-child) {
    margin-bottom: 0;
}

.prose:deep(strong) {
    font-weight: 700;
}

.prose:deep(a) {
    color: #1976d2;
    text-decoration: underline;
    text-underline-offset: 0.125rem;
}

.prose:deep(ul),
.prose:deep(ol) {
    margin: 0 0 0.5rem;
    padding-left: 1.25rem;
}

.prose:deep(ul:last-child),
.prose:deep(ol:last-child) {
    margin-bottom: 0;
}

.description-editor {
    border-radius: 0.625rem;
    overflow: hidden;
    border: 0.0625rem solid rgb(var(--v-theme-outline-variant, 234, 236, 240));
}

.description-editor:deep(.ql-toolbar.ql-snow) {
    display: flex;
    align-items: center;
    gap: 0.125rem;
    padding: 0.375rem 0.5rem;
    border: none;
    border-bottom: 0.0625rem solid
        rgb(var(--v-theme-outline-variant, 234, 236, 240));
    background: rgb(var(--v-theme-grey-lighten-4, 245, 246, 248));
}

.description-editor:deep(.ql-toolbar.ql-snow .ql-formats) {
    margin-right: 0.5rem;
}

.description-editor:deep(.ql-toolbar.ql-snow button) {
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 0.375rem;
    transition: background-color 0.12s ease;
}

.description-editor:deep(.ql-toolbar.ql-snow button:hover) {
    background: rgb(var(--v-theme-surface));
}

.description-editor:deep(.ql-toolbar.ql-snow button.ql-active) {
    background: rgba(25, 118, 210, 0.1);
}

.description-editor:deep(.ql-toolbar.ql-snow .ql-stroke) {
    stroke: rgb(var(--v-theme-text-secondary, 71, 84, 103));
}

.description-editor:deep(.ql-toolbar.ql-snow .ql-fill) {
    fill: rgb(var(--v-theme-text-secondary, 71, 84, 103));
}

.description-editor:deep(.ql-toolbar.ql-snow button:hover .ql-stroke),
.description-editor:deep(.ql-toolbar.ql-snow button.ql-active .ql-stroke) {
    stroke: #1976d2;
}

.description-editor:deep(.ql-toolbar.ql-snow button:hover .ql-fill),
.description-editor:deep(.ql-toolbar.ql-snow button.ql-active .ql-fill) {
    fill: #1976d2;
}

.description-editor:deep(.ql-container.ql-snow) {
    border: none;
    font-family: inherit;
    font-size: 0.8125rem;
}

.description-editor:deep(.ql-editor) {
    min-height: 6rem;
    padding: 0.625rem 0.75rem;
    color: rgb(var(--v-theme-on-surface));
    line-height: 1.5;
}

.description-editor:deep(.ql-editor.ql-blank::before) {
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    font-style: normal;
}
</style>
