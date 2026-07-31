<template>
    <v-container fluid class="pa-6">
        <div class="d-flex align-center mb-4">
            <div>
                <h1 class="text-h5 font-weight-medium">Notifications</h1>
                <span class="text-body-2 text-medium-emphasis">
                    {{ unreadCount }} unread
                </span>
            </div>
            <v-spacer />
            <v-btn
                variant="text"
                size="small"
                :disabled="unreadCount === 0"
                @click="markAllRead"
            >
                Mark all as read
            </v-btn>
        </div>

        <v-tabs v-model="filter" class="mb-4">
            <v-tab value="all">All</v-tab>
            <v-tab value="unread">Unread</v-tab>
            <v-tab value="mentions">Mentions</v-tab>
        </v-tabs>
        <v-divider class="mb-2" />

        <v-list v-if="filteredNotifications.length" lines="two">
            <v-list-item
                v-for="notification in filteredNotifications"
                :key="notification.id"
                :class="{ 'bg-primary-lighten-5': !notification.read }"
                @click="markRead(notification.id)"
            >
                <template #prepend>
                    <v-badge
                        :model-value="!notification.read"
                        color="error"
                        dot
                        location="top end"
                    >
                        <v-avatar color="primary" size="36">
                            <span class="text-body-2">{{
                                notification.actorInitials
                            }}</span>
                        </v-avatar>
                    </v-badge>
                </template>

                <v-list-item-title class="text-body-2">
                    <strong>{{ notification.actor }}</strong>
                    {{ notification.action }}
                </v-list-item-title>
                <v-list-item-subtitle>{{
                    notification.context
                }}</v-list-item-subtitle>

                <template #append>
                    <div class="d-flex flex-column align-end">
                        <v-icon
                            :icon="typeIcon(notification.type)"
                            size="16"
                            class="mb-1"
                        />
                        <span class="text-caption text-medium-emphasis">{{
                            notification.time
                        }}</span>
                    </div>
                </template>
            </v-list-item>
        </v-list>

        <v-sheet v-else class="pa-8 text-center" border rounded>
            <v-icon
                icon="mdi-bell-check-outline"
                size="32"
                class="mb-2 text-medium-emphasis"
            />
            <div class="text-body-2 text-medium-emphasis">
                You're all caught up
            </div>
        </v-sheet>
    </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

const notifications = ref([
    {
        id: 1,
        actor: "Maya Chen",
        actorInitials: "MC",
        action: "commented on Homepage wireframes",
        context: 'Website Redesign · "Can we try a lighter hero image?"',
        time: "10 min ago",
        type: "comment",
        read: false,
    },
    {
        id: 2,
        actor: "Devon Ray",
        actorInitials: "DR",
        action: "completed Set up staging environment",
        context: "Mobile App",
        time: "1 hr ago",
        type: "task",
        read: false,
    },
    {
        id: 3,
        actor: "Priya Nair",
        actorInitials: "PN",
        action: "mentioned you in Sprint Retro Notes",
        context: '"@jordan can you confirm the release date?"',
        time: "3 hr ago",
        type: "mention",
        read: false,
    },
    {
        id: 4,
        actor: "Devon Ray",
        actorInitials: "DR",
        action: "assigned you Review API contract",
        context: "Mobile App · due Tomorrow",
        time: "5 hr ago",
        type: "assignment",
        read: true,
    },
    {
        id: 5,
        actor: "Maya Chen",
        actorInitials: "MC",
        action: "updated Approve campaign copy",
        context: "Marketing Campaign · priority changed to Low",
        time: "Yesterday",
        type: "task",
        read: true,
    },
]);

const filter = ref("all");

const filteredNotifications = computed(() => {
    if (filter.value === "unread")
        return notifications.value.filter((n) => !n.read);
    if (filter.value === "mentions")
        return notifications.value.filter((n) => n.type === "mention");
    return notifications.value;
});

const unreadCount = computed(
    () => notifications.value.filter((n) => !n.read).length,
);

function markRead(id) {
    const notification = notifications.value.find((n) => n.id === id);
    if (notification) notification.read = true;
}

function markAllRead() {
    notifications.value.forEach((n) => (n.read = true));
}

function typeIcon(type) {
    return (
        {
            comment: "mdi-comment-outline",
            task: "mdi-checkbox-marked-outline",
            mention: "mdi-at",
            assignment: "mdi-account-arrow-right-outline",
        }[type] ?? "mdi-bell-outline"
    );
}
</script>
