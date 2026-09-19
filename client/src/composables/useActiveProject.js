import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";

export function useActiveProject() {
    const { currentUser } = useAuthStore();

    const projectId = computed(() => {
        if (!currentUser?.active_project_public_id) {
            throw new Error("Authenticated user has no active project");
        }

        return currentUser.active_project_public_id;
    });

    return {
        projectId,
    };
}
