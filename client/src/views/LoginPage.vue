<script setup>
import { useRouter } from "vue-router";
import { reactive, ref } from "vue";
import { useAuthStore } from "@/stores/auth";

/** @typedef {import("vue").Ref<InstanceType<typeof import("vuetify/components").VForm> | null>} VFormRef */

const router = useRouter();
const authStore = useAuthStore();

/** @type {VFormRef} */
const formRef = ref(null);

const form = reactive({
    username: "",
    password: "",
    showPassword: false,
    isLoading: false,
    errorMessage: "",
});

const rules = {
    username: (/** @type {string} */ v) =>
        !!v?.trim() || "Username is required",

    validUsername: (/** @type {string} */ v) =>
        !v || /^[a-zA-Z0-9]+$/.test(v) || "Username must be alphanumeric",

    password: (/** @type {string} */ v) => !!v || "Password is required",
};

async function handleSubmit() {
    if (!formRef.value) return;

    form.errorMessage = "";

    const { valid } = await formRef.value.validate();
    if (!valid) return;

    form.isLoading = true;

    try {
        await authStore.login({
            username: form.username,
            password: form.password,
        });

        router.push("/");
    } catch (error) {
        if (error instanceof Error && error.message === "Invalid credentials") {
            form.errorMessage = "Invalid username or password.";
        } else {
            form.errorMessage = "Something went wrong.";
        }
    } finally {
        form.isLoading = false;
    }
}
</script>

<template>
    <div class="login-wrapper">
        <v-card class="login-card" variant="outlined">
            <div class="card-header">
                <h1 class="text-h6 font-weight-bold card-title">Sign in</h1>

                <p class="text-caption text-medium-emphasis mb-0 mt-1">
                    Sign in to continue to your workspace.
                </p>
            </div>

            <v-divider />

            <v-card-text class="pa-5">
                <v-form ref="formRef" @submit.prevent="handleSubmit">
                    <v-alert
                        v-if="form.errorMessage"
                        type="error"
                        variant="tonal"
                        density="compact"
                        class="mb-4"
                    >
                        {{ form.errorMessage }}
                    </v-alert>

                    <div class="form-group mb-4">
                        <label class="field-label">
                            Username
                            <span class="required-mark">*</span>
                        </label>

                        <v-text-field
                            v-model="form.username"
                            type="username"
                            placeholder="you@example.com"
                            :rules="[rules.username, rules.validUsername]"
                            variant="outlined"
                            density="compact"
                            hide-details="auto"
                            autofocus
                            autocomplete="username"
                            class="custom-field"
                        />
                    </div>

                    <div class="form-group mb-2">
                        <label class="field-label">
                            Password
                            <span class="required-mark">*</span>
                        </label>

                        <v-text-field
                            v-model="form.password"
                            :type="form.showPassword ? 'text' : 'password'"
                            placeholder="Enter your password"
                            :rules="[rules.password]"
                            variant="outlined"
                            density="compact"
                            hide-details="auto"
                            autocomplete="current-password"
                            class="custom-field"
                            :append-inner-icon="
                                form.showPassword
                                    ? 'mdi-eye-off-outline'
                                    : 'mdi-eye-outline'
                            "
                            @click:append-inner="
                                form.showPassword = !form.showPassword
                            "
                        />
                    </div>

                    <div class="d-flex justify-end mb-5">
                        <v-btn
                            variant="text"
                            color="primary"
                            density="compact"
                            class="text-none px-0"
                            type="button"
                            @click="router.push('/forgot-password')"
                        >
                            Forgot password?
                        </v-btn>
                    </div>

                    <v-btn
                        type="submit"
                        color="primary"
                        variant="flat"
                        block
                        density="comfortable"
                        class="text-none font-weight-medium"
                        :loading="form.isLoading"
                        :disabled="form.isLoading"
                    >
                        Sign In
                    </v-btn>
                </v-form>
            </v-card-text>

            <v-divider />

            <div class="card-footer">
                <span class="text-caption text-medium-emphasis">
                    Don't have an account?
                </span>

                <v-btn
                    variant="text"
                    color="primary"
                    density="compact"
                    class="text-none font-weight-medium ml-1"
                    @click="router.push('/register')"
                >
                    Create an account
                </v-btn>
            </div>
        </v-card>
    </div>
</template>

<style scoped>
.login-wrapper {
    min-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    background-color: #f4f5f7;
}

.login-card {
    width: 100%;
    max-width: 32.5rem;
    background-color: #fff;
    border: 1px solid #e1e4e8;
    border-radius: 0.5rem;
    box-shadow: none;
}

.card-header {
    padding: 1.25rem 1.25rem 1rem;
}

.card-title {
    color: #1a1f2c;
    line-height: 1.2;
    letter-spacing: -0.01em;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.field-label {
    margin-bottom: 0.375rem;
    font-size: 0.8125rem;
    font-weight: 600;
    color: #344054;
}

.required-mark {
    color: #d92d20;
}

.card-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.875rem 1.25rem;
}

:deep(.v-field) {
    background-color: #fff;
    border-radius: 0.375rem;
}

:deep(.v-field--outlined .v-field__outline) {
    --v-field-border-opacity: 1;
    color: #d0d5dd;
}

:deep(.v-field--focused .v-field__outline) {
    color: rgb(var(--v-theme-primary));
}

:deep(.v-btn) {
    border-radius: 0.375rem;
    box-shadow: none;
}
</style>
