<template>
    <v-container fluid class="pa-6">
        <h1 class="text-h5 font-weight-medium mb-6">Settings</h1>

        <v-row>
            <!-- Section nav -->
            <v-col cols="12" md="3">
                <v-list nav density="compact">
                    <v-list-item
                        v-for="section in sections"
                        :key="section.value"
                        :active="activeSection === section.value"
                        :prepend-icon="section.icon"
                        :title="section.label"
                        @click="activeSection = section.value"
                    />
                </v-list>
            </v-col>

            <!-- Panel -->
            <v-col cols="12" md="9">
                <!-- Profile -->
                <v-card v-if="activeSection === 'profile'" variant="outlined" class="pa-4">
                    <v-card-title class="text-subtitle-1 font-weight-medium px-0">Profile</v-card-title>
                    <v-divider class="mb-4" />
                    <div class="d-flex align-center mb-4">
                        <v-avatar color="primary" size="56" class="mr-4">
                            <span class="text-h6">{{ profile.initials }}</span>
                        </v-avatar>
                        <v-btn variant="outlined" size="small">Change photo</v-btn>
                    </div>
                    <v-text-field v-model="profile.name" label="Full name" variant="outlined" density="comfortable" class="mb-2" />
                    <v-text-field v-model="profile.email" label="Email" variant="outlined" density="comfortable" class="mb-2" />
                    <v-text-field v-model="profile.role" label="Role" variant="outlined" density="comfortable" />
                    <v-card-actions class="px-0">
                        <v-spacer />
                        <v-btn color="primary" variant="flat">Save changes</v-btn>
                    </v-card-actions>
                </v-card>

                <!-- Theme -->
                <v-card v-else-if="activeSection === 'theme'" variant="outlined" class="pa-4">
                    <v-card-title class="text-subtitle-1 font-weight-medium px-0">Theme</v-card-title>
                    <v-divider class="mb-4" />
                    <v-radio-group v-model="theme.mode" inline>
                        <v-radio label="Light" value="light" />
                        <v-radio label="Dark" value="dark" />
                        <v-radio label="Match system" value="system" />
                    </v-radio-group>
                    <v-switch v-model="theme.compact" label="Compact density" color="primary" hide-details class="mt-2" />
                </v-card>

                <!-- Notifications -->
                <v-card v-else-if="activeSection === 'notifications'" variant="outlined" class="pa-4">
                    <v-card-title class="text-subtitle-1 font-weight-medium px-0">Notifications</v-card-title>
                    <v-divider class="mb-2" />
                    <v-list>
                        <v-list-item v-for="pref in notificationPrefs" :key="pref.key">
                            <v-list-item-title>{{ pref.label }}</v-list-item-title>
                            <v-list-item-subtitle>{{ pref.hint }}</v-list-item-subtitle>
                            <template #append>
                                <v-switch v-model="pref.enabled" color="primary" hide-details />
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>

                <!-- Integrations -->
                <v-card v-else-if="activeSection === 'integrations'" variant="outlined" class="pa-4">
                    <v-card-title class="text-subtitle-1 font-weight-medium px-0">Integrations</v-card-title>
                    <v-divider class="mb-2" />
                    <v-list>
                        <v-list-item v-for="integration in integrations" :key="integration.name" :prepend-icon="integration.icon">
                            <v-list-item-title>{{ integration.name }}</v-list-item-title>
                            <v-list-item-subtitle>{{ integration.connected ? "Connected" : "Not connected" }}</v-list-item-subtitle>
                            <template #append>
                                <v-btn
                                    :color="integration.connected ? undefined : 'primary'"
                                    :variant="integration.connected ? 'outlined' : 'flat'"
                                    size="small"
                                    @click="integration.connected = !integration.connected"
                                >
                                    {{ integration.connected ? "Disconnect" : "Connect" }}
                                </v-btn>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, reactive } from "vue";

const sections = [
    { value: "profile", label: "Profile", icon: "mdi-account-outline" },
    { value: "theme", label: "Theme", icon: "mdi-palette-outline" },
    { value: "notifications", label: "Notifications", icon: "mdi-bell-outline" },
    { value: "integrations", label: "Integrations", icon: "mdi-puzzle-outline" },
];

const activeSection = ref("profile");

const profile = reactive({
    name: "Jordan Lee",
    email: "jordan@patapim.app",
    role: "Product Designer",
    initials: "JL",
});

const theme = reactive({
    mode: "system",
    compact: false,
});

const notificationPrefs = reactive([
    { key: "comments", label: "Comments", hint: "New comments on tasks and documents", enabled: true },
    { key: "assignments", label: "Assignments", hint: "When a task is assigned to you", enabled: true },
    { key: "deadlines", label: "Deadline reminders", hint: "Tasks due within 24 hours", enabled: true },
    { key: "digest", label: "Weekly digest", hint: "Summary email every Monday", enabled: false },
]);

const integrations = reactive([
    { name: "Slack", icon: "mdi-slack", connected: true },
    { name: "GitHub", icon: "mdi-github", connected: true },
    { name: "Google Drive", icon: "mdi-google-drive", connected: false },
]);
</script>
