import { computed, reactive, ref, watch } from "vue";
import { useTasksStore } from "@/stores/tasks.store";
import {
    isTaskOverdue,
    parseTags,
    serializeTags,
} from "@/utils/taskFormatters";

/**
 * @typedef {import("@/types/task").TaskRead} TaskRead
 * @typedef {import("@/types/task").TaskDraft} TaskDraft
 * @typedef {import("@/types/task").TaskCreate} TaskCreate
 * @typedef {import("@/types/shared").EditMode} EditMode
 */

/**
 * @param {import("vue").Ref<TaskRead | null>} task
 * @param {String} taskId
 */
export function useTaskEditor(task, taskId) {
    const tasksStore = useTasksStore();

    const editMode = ref(/** @type {EditMode} */ ("none"));

    const isSaving = ref(false);

    const isSavingStatus = ref(false);
    const isSavingPriority = ref(false);

    const draft = reactive(getTaskDraft(null));
    const initialDraft = reactive(getTaskDraft(null));

    const hasPendingChanges = computed(
        () => JSON.stringify(draft) !== JSON.stringify(initialDraft)
    );

    /** @type {import("vue").Ref<TaskRead["status"] | null>} */
    const selectedStatus = ref(task.value?.status ?? null);

    /** @type {import("vue").Ref<TaskRead["priority"] | null>} */
    const selectedPriority = ref(task.value?.priority ?? null);

    const isEditingTitle = computed(() => editMode.value === "title");
    const isEditingBody = computed(() => editMode.value === "body");
    const isEditingDetails = computed(() => editMode.value === "details");
    const isEditingTags = computed(() => editMode.value === "tags");

    const isOverdue = computed(() =>
        task.value ? isTaskOverdue(task.value) : false
    );

    const startDate = computed({
        get() {
            return toDateInput(draft.start_date);
        },
        set(value) {
            draft.start_date = value;
        },
    });

    const dueDate = computed({
        get() {
            return toDateInput(draft.due_date);
        },
        set(value) {
            draft.due_date = value;
        },
    });

    const tags = computed({
        get() {
            return parseTags(draft.tags);
        },
        set(value) {
            draft.tags = serializeTags(value);
        },
    });

    watch(task, setSelectedTaskData, { immediate: true });

    /** @param {TaskRead | null} newTask */
    function setSelectedTaskData(newTask) {
        if (!newTask) return;

        selectedStatus.value = newTask.status;
        selectedPriority.value = newTask.priority;

        if (editMode.value === "none") {
            syncDraftFromTask();
        }
    }

    function syncDraftFromTask() {
        const values = getTaskDraft(task.value);

        copyDraftValues(draft, values);
        copyDraftValues(initialDraft, values);
    }

    /** @param {EditMode} mode */
    function beginEdit(mode) {
        if (editMode.value === "none") {
            syncDraftFromTask();
        }

        editMode.value = mode;
    }

    function cancelChanges() {
        copyDraftValues(draft, initialDraft);

        editMode.value = "none";
    }

    async function saveChanges() {
        if (!task.value || !hasPendingChanges.value) {
            editMode.value = "none";
            return;
        }

        isSaving.value = true;

        try {
            const payload = buildUpdatePayload(draft, initialDraft);

            await tasksStore.update(taskId, payload);

            copyDraftValues(initialDraft, draft);

            editMode.value = "none";
        } finally {
            isSaving.value = false;
        }
    }

    /**
     * @param {"status" | "priority"} field
     * @param {{ value: string }} item
     * @param {import("vue").Ref<string | null>} localRef
     * @param {import("vue").Ref<boolean>} savingRef
     */
    async function updateTaskField(field, item, localRef, savingRef) {
        if (!task.value) return;

        const previousValue = task.value[field];

        savingRef.value = true;

        try {
            await tasksStore.update(taskId, {
                [field]: item.value,
            });
        } catch (error) {
            localRef.value = previousValue;
            throw error;
        } finally {
            savingRef.value = false;
        }
    }

    /** @param {{ value: string }} item */
    function onStatusChange(item) {
        return updateTaskField("status", item, selectedStatus, isSavingStatus);
    }

    /** @param {{ value: string }} item */
    function onPriorityChange(item) {
        return updateTaskField(
            "priority",
            item,
            selectedPriority,
            isSavingPriority
        );
    }

    return {
        editMode,
        draft,

        isSaving,
        hasPendingChanges,

        isEditingTitle,
        isEditingBody,
        isEditingDetails,
        isEditingTags,

        selectedStatus,
        selectedPriority,

        isSavingStatus,
        isSavingPriority,

        isOverdue,

        startDate,
        dueDate,
        tags,

        beginEdit,
        cancelChanges,
        saveChanges,

        onStatusChange,
        onPriorityChange,
    };
}

/** @param {String | null} value */
function toDateInput(value) {
    return value ? new Date(value).toISOString().slice(0, 10) : "";
}

/**
 * @param {TaskRead | null} [source]
 * @returns {TaskDraft}
 */
function getTaskDraft(source) {
    return {
        title: source?.title ?? "",
        description: source?.description ?? "",
        tags: source?.tags ?? "",
        status: source?.status ?? null,
        priority: source?.priority ?? null,
        start_date: source?.start_date ?? null,
        due_date: source?.due_date ?? null,
    };
}

/**
 * @param {TaskDraft} target
 * @param {TaskDraft} source
 */
function copyDraftValues(target, source) {
    Object.assign(target, source);
}

/**
 * @param {TaskDraft} draft
 * @param {TaskDraft} initialDraft
 * @returns {Partial<TaskCreate>}
 */
function buildUpdatePayload(draft, initialDraft) {
    /** @type {Partial<TaskCreate>} */
    const payload = {};

    for (const field of Object.keys(draft)) {
        // @ts-ignore
        if (draft[field] !== initialDraft[field]) payload[field] = draft[field];
    }

    if (payload.status === null) {
        delete payload.status;
    }

    if (payload.priority === null) {
        delete payload.priority;
    }

    return payload;
}
