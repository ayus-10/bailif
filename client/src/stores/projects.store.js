import { defineStore } from "pinia";

import { getProject } from "@/api/projects.api";
import { createResourceStore } from "@/stores/factories/createResourceStore";

const projectsResource = createResourceStore(
    /** @param {string} projectId */
    (projectId) => getProject(projectId)
);

export const useProjectsStore = defineStore("projects", {
    state: () => projectsResource.state,
    actions: projectsResource.actions,
});
