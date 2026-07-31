<template>
    <v-container fluid class="pa-0 fill-height">
        <v-row no-gutters class="fill-height">
            <!-- Document list -->
            <v-col cols="12" md="3" class="border-e fill-height">
                <div class="d-flex align-center pa-4">
                    <span class="text-subtitle-1 font-weight-medium"
                        >Documents</span
                    >
                    <v-spacer />
                    <v-btn
                        icon="mdi-plus"
                        size="small"
                        variant="text"
                        @click="createDocument"
                    />
                </div>
                <v-divider />
                <v-list density="comfortable" nav>
                    <v-list-item
                        v-for="doc in documents"
                        :key="doc.id"
                        :active="doc.id === activeDoc.id"
                        prepend-icon="mdi-file-document-outline"
                        :title="doc.title"
                        :subtitle="`edited ${doc.updated}`"
                        @click="activeDocId = doc.id"
                    />
                </v-list>
            </v-col>

            <!-- Editor -->
            <v-col cols="12" md="9" class="fill-height d-flex flex-column">
                <div class="d-flex align-center pa-4">
                    <v-text-field
                        v-model="activeDoc.title"
                        variant="plain"
                        density="compact"
                        hide-details
                        class="text-h6 font-weight-medium"
                    />
                    <v-spacer />
                    <v-avatar-group class="mr-3">
                        <v-avatar
                            v-for="c in activeDoc.collaborators"
                            :key="c"
                            color="primary"
                            size="26"
                        >
                            <span class="text-caption">{{ c }}</span>
                        </v-avatar>
                    </v-avatar-group>
                    <v-chip
                        size="small"
                        color="success"
                        variant="tonal"
                        prepend-icon="mdi-circle-medium"
                    >
                        Saved
                    </v-chip>
                </div>
                <v-divider />

                <!-- Formatting toolbar -->
                <div class="d-flex align-center pa-2">
                    <v-btn
                        icon="mdi-format-bold"
                        variant="text"
                        size="small"
                        @click="format('bold')"
                    />
                    <v-btn
                        icon="mdi-format-italic"
                        variant="text"
                        size="small"
                        @click="format('italic')"
                    />
                    <v-btn
                        icon="mdi-format-underline"
                        variant="text"
                        size="small"
                        @click="format('underline')"
                    />
                    <v-divider vertical class="mx-2" />
                    <v-btn
                        icon="mdi-format-list-bulleted"
                        variant="text"
                        size="small"
                        @click="format('insertUnorderedList')"
                    />
                    <v-btn
                        icon="mdi-format-list-numbered"
                        variant="text"
                        size="small"
                        @click="format('insertOrderedList')"
                    />
                    <v-divider vertical class="mx-2" />
                    <v-btn
                        icon="mdi-link-variant"
                        variant="text"
                        size="small"
                        @click="insertLink"
                    />
                </div>
                <v-divider />

                <div
                    ref="editorRef"
                    class="editor-surface pa-6 flex-grow-1"
                    contenteditable="true"
                    @input="onInput"
                    v-html="activeDoc.content"
                />
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const documents = ref([
    {
        id: 1,
        title: "Website Redesign — Brief",
        updated: "10 min ago",
        collaborators: ["MC", "DR"],
        content: "<p>Goals, scope, and success metrics for the redesign.</p>",
    },
    {
        id: 2,
        title: "Sprint Retro Notes",
        updated: "yesterday",
        collaborators: ["PN"],
        content: "<p>What went well, what didn't, action items.</p>",
    },
]);

const activeDocId = ref(documents.value[0].id);
const activeDoc = computed(() =>
    documents.value.find((d) => d.id === activeDocId.value),
);
const editorRef = ref(null);

function onInput(event) {
    activeDoc.value.content = event.target.innerHTML;
}

function format(command) {
    document.execCommand(command, false, null);
    editorRef.value?.focus();
}

function insertLink() {
    const url = window.prompt("Link URL");
    if (url) {
        document.execCommand("createLink", false, url);
    }
}

function createDocument() {
    const id = Math.max(...documents.value.map((d) => d.id)) + 1;
    documents.value.push({
        id,
        title: "Untitled Document",
        updated: "just now",
        collaborators: [],
        content: "<p></p>",
    });
    activeDocId.value = id;
}
</script>

<style scoped>
.editor-surface {
    outline: none;
    overflow-y: auto;
    line-height: 1.6;
}

.editor-surface:focus {
    outline: none;
}
</style>
