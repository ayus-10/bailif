<!-- CheckboxRichEditor.vue -->
<!--
  Wrapper around <QuillEditor> that adds a custom, stateful checkbox embed.

  Usage:
    <CheckboxRichEditor
      v-model:content="doc"      // Quill delta
      v-model:tasks="taskState"  // { [id]: { checked, label } }
      @checkbox-toggle="onToggle"
    />

  `tasks` is two-way bound: toggling a checkbox in the editor updates it
  (and emits update:tasks to the parent), and if the parent mutates it
  from outside (e.g. after an API refresh), the change is pushed back
  into the editor DOM automatically.
-->
<template>
    <QuillEditor
        ref="editorRef"
        v-model:content="content"
        content-type="delta"
        :modules="modules"
        :toolbar="resolvedToolbar"
        :placeholder="placeholder"
        :read-only="readOnly"
        :theme="theme"
        @ready="onReady"
        @text-change="(...args) => emit('text-change', ...args)"
    />
</template>

<script setup>
import { Quill, QuillEditor } from "@vueup/vue-quill";
import { computed, ref, watch } from "vue";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "./customCheckboxBlot";
import { syncCheckboxState } from "./customCheckboxBlot";

const props = defineProps({
    placeholder: { type: String, default: "" },
    readOnly: { type: Boolean, default: false },
    theme: { type: String, default: "snow" },
    // Base toolbar groups. The "customCheckbox" button is appended
    // automatically if you don't already include it.
    toolbar: {
        type: Array,
        default: () => [
            ["bold", "italic", "underline"],
            [{ list: "ordered" }, { list: "bullet" }],
        ],
    },
});

const emit = defineEmits(["ready", "text-change", "checkbox-toggle"]);

// The document itself.
const content = defineModel("content", {
    default: () => ({ ops: [{ insert: "\n" }] }),
});

// App-level task state keyed by checkbox id — this is the "synced to
// app state" part. Two-way bound so a parent can read toggles AND push
// external changes back in.
const tasks = defineModel("tasks", { default: () => ({}) });

const editorRef = ref(null);
let quill = null;

const resolvedToolbar = computed(() => {
    const hasCheckbox = props.toolbar.some((group) =>
        Array.isArray(group)
            ? group.includes("customCheckbox")
            : group === "customCheckbox"
    );
    return hasCheckbox ? props.toolbar : [...props.toolbar, ["customCheckbox"]];
});

// NOTE: vue-quill builds the underlying Quill instance once on mount from
// this modules config. Changing `toolbar` after mount won't rebuild the
// toolbar UI — that's a Quill limitation, not something this wrapper works
// around. Set it once when the component is created.
const modules = computed(() => ({
    toolbar: {
        container: resolvedToolbar.value,
        handlers: {
            customCheckbox: () => insertCheckbox(),
        },
    },
}));

function insertCheckbox(label = "New task") {
    if (!quill) return null;
    const range = quill.getSelection(true) ?? { index: quill.getLength() };
    const id = crypto.randomUUID();

    tasks.value = { ...tasks.value, [id]: { checked: false, label } };

    quill.insertEmbed(
        range.index,
        "customCheckbox",
        { id, checked: false, label },
        Quill.sources.USER
    );
    quill.insertText(range.index + 1, " ", Quill.sources.SILENT);
    quill.setSelection(range.index + 2, Quill.sources.SILENT);
    return id;
}

function onReady(quillInstance) {
    quill = quillInstance;
    quill.root.addEventListener("checkbox-toggle", (e) => {
        const { id, checked } = e.detail;
        if (tasks.value[id]) {
            tasks.value = {
                ...tasks.value,
                [id]: { ...tasks.value[id], checked },
            };
        }
        emit("checkbox-toggle", { id, checked });
    });
    emit("ready", quillInstance);
}

// External task-state changes (e.g. an API refresh) get pushed into the DOM.
watch(
    tasks,
    (newTasks) => {
        if (!quill) return;
        for (const [id, task] of Object.entries(newTasks)) {
            syncCheckboxState(quill, id, task.checked);
        }
    },
    { deep: true }
);

function syncCheckboxState(quillInstance, id, checked) {
    const node = quillInstance.root.querySelector(
        `.ql-custom-checkbox[data-id="${id}"]`
    );
    if (!node) return;
    node.setAttribute("data-checked", String(checked));
    const input = node.querySelector('input[type="checkbox"]');
    if (input) input.checked = checked;
}

defineExpose({
    getQuill: () => quill,
    insertCheckbox,
    focus: () => quill?.focus(),
});
</script>

<style>
.ql-custom-checkbox {
    display: inline-flex;
    align-items: center;
    gap: 0.4em;
    margin: 0 0.15em;
}
.ql-custom-checkbox input[type="checkbox"] {
    cursor: pointer;
}
.ql-toolbar .ql-customCheckbox::before {
    content: "☑";
    font-size: 16px;
}
</style>
