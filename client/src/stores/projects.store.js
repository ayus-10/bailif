import { defineStore } from "pinia";

import { fetchProject } from "@/api/projects.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const projectsResource = createResourceStore(
    /** @param {string} projectId */
    (projectId) => fetchProject(projectId)
);

export const useProjectsStore = defineStore("projects", {
    state: () => projectsResource.state,
    actions: projectsResource.actions,
});
