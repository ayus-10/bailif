import { defineStore } from "pinia";
import { apiFetch } from "@/api/client";
import { ApiError, parseJson } from "@/api/shared.api";
import { resetSessionData } from "@/utils/sessionReset";

/**
 * @typedef {Object} User
 * @property {number} public_id
 * @property {string} username
 * @property {number} active_project_public_id
 */

/**
 * @typedef {Object} AuthState
 * @property {string | null} accessToken
 * @property {User | null} currentUser
 * @property {boolean} isInitializing
 */

export const useAuthStore = defineStore("auth", {
    /**
     * @returns {AuthState}
     */
    state: () => ({
        accessToken: null,
        currentUser: null,
        isInitializing: true,
    }),

    getters: {
        isAuthenticated: (state) =>
            state.accessToken !== null && state.currentUser !== null,
        isOnboardingComplete: (state) =>
            !!state.currentUser?.active_project_public_id,
    },

    actions: {
        /**
         * @param {string} token
         */
        setAccessToken(token) {
            this.accessToken = token;
        },

        clearSession() {
            this.accessToken = null;
            this.currentUser = null;
            resetSessionData();
        },

        /**
         * @param {number} projectPublicId
         * @throws {ApiError}
         */
        async setActiveProject(projectPublicId) {
            const res = await apiFetch("/users/me", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    active_project_public_id: projectPublicId,
                }),
            });

            this.currentUser = await parseJson(res);
        },

        /**
         * @param {{ username: string, password: string }} params
         * @throws {ApiError}
         */
        async login({ username, password }) {
            const form = new URLSearchParams();
            form.set("username", username);
            form.set("password", password);

            const res = await apiFetch("/auth/login", {
                method: "POST",
                skipAuth: true,
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: form,
            });

            if (!res.ok) {
                throw new ApiError("Invalid credentials", { status: 401 });
            }

            const data = await res.json();
            this.accessToken = data.token;

            await this.fetchCurrentUser();

            if (!this.isAuthenticated) {
                throw new ApiError("Unable to load your account", {
                    status: 401,
                });
            }
        },

        async fetchCurrentUser() {
            const res = await apiFetch("/users/me");
            if (res.ok) {
                this.currentUser = await res.json();
            } else {
                this.clearSession();
            }
        },

        /**
         * @throws {ApiError}
         */
        async refreshCurrentUser() {
            const res = await apiFetch("/users/me");

            if (res.status === 401) {
                this.clearSession();
                return;
            }

            if (!res.ok) {
                throw new ApiError("Failed to refresh user", {
                    status: res.status,
                });
            }

            this.currentUser = await res.json();
        },

        async logout() {
            await apiFetch("/auth/logout", { method: "POST" }).catch(() => {});
            this.clearSession();
        },

        // Called once at app startup
        async initialize() {
            this.isInitializing = true;
            try {
                const res = await apiFetch("/auth/refresh", {
                    method: "POST",
                    skipAuth: true,
                });

                if (res.ok) {
                    const data = await res.json();
                    this.accessToken = data.token;
                    await this.fetchCurrentUser();
                }
            } finally {
                this.isInitializing = false;
            }
        },
    },
});
