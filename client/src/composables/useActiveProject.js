import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";

export function useActiveProject() {
    const auth = useAuthStore();

    const projectId = computed(
        () => auth.currentUser?.active_project_public_id ?? null
    );

    return { projectId };
}
