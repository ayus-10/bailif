import { defineStore } from "pinia";
import { apiFetch } from "@/api/client";

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
    /** @returns {AuthState} */
    state: () => ({
        accessToken: null,
        currentUser: null,
        isInitializing: true,
    }),

    getters: {
        isAuthenticated: (state) =>
            state.accessToken !== null && state.currentUser !== null,
    },

    actions: {
        /** @param {string} token */
        setAccessToken(token) {
            this.accessToken = token;
        },

        clearSession() {
            this.accessToken = null;
            this.currentUser = null;
        },

        /**
         * @param {{ username: string, password: string }} params
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
                throw new Error("Invalid credentials");
            }

            const data = await res.json();
            this.accessToken = data.token;

            await this.fetchCurrentUser();
        },

        async fetchCurrentUser() {
            const res = await apiFetch("/users/me");
            if (res.ok) {
                this.currentUser = await res.json();
            } else {
                this.clearSession();
            }
        },

        async refreshCurrentUser() {
            const res = await apiFetch("/users/me");

            if (res.status === 401) {
                this.clearSession();
                return;
            }
            if (!res.ok) throw new Error("Failed to refresh user");

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
