<script setup>
import { Ripple as vRipple } from "vuetify/directives";
import { computed } from "vue";
import { toasts, useToast } from "@/composables/useToast";
import { useWindowBlurred } from "@/composables/useWindowBlurred";
import { TOAST_POSITIONS } from "@/constants/toast";

/**
 * @typedef {import("@/types/toast").ToastItem} ToastItem
 */

const toast = useToast();
const windowBlurred = useWindowBlurred();

const grouped = computed(() =>
    Object.fromEntries(
        TOAST_POSITIONS.map((position) => [
            position,
            toasts.filter((t) => t.position === position),
        ])
    )
);

/**
 * @param {ToastItem} t
 * @returns {boolean}
 */
function isPaused(t) {
    return t.paused || (windowBlurred.value && t.pauseOnFocusLoss);
}

/**
 * @param {ToastItem} t
 */
function onToastClick(t) {
    t.onClick?.(t);
    if (t.closeOnClick) toast.dismiss(t.id);
}
</script>

<template>
    <TransitionGroup
        v-for="position in TOAST_POSITIONS"
        :key="position"
        tag="div"
        name="toast"
        aria-live="polite"
        :class="['toast-stack', `toast-stack--${position}`]"
    >
        <div
            v-for="t in grouped[position]"
            :key="t.id"
            class="toast"
            :class="[
                `toast--${t.type}`,
                { 'toast--clickable': t.closeOnClick || t.onClick },
            ]"
            :role="t.type === 'error' ? 'alert' : 'status'"
            @mouseenter="t.paused = t.pauseOnHover"
            @mouseleave="t.paused = false"
            @click="onToastClick(t)"
        >
            <v-icon
                v-if="t.iconName"
                :icon="t.iconName"
                size="1.125rem"
                class="toast__icon"
            />

            <div class="toast__body">
                <component
                    v-if="t.hasComponent && typeof t.content === 'object'"
                    :is="t.content.component"
                    v-bind="t.content.props"
                />
                <template v-else>{{ t.content }}</template>
            </div>

            <button
                v-if="t.showCloseButton"
                v-ripple
                type="button"
                class="toast__close"
                aria-label="Dismiss notification"
                @click.stop="toast.dismiss(t.id)"
            >
                <v-icon icon="mdi-close" size="1rem" />
            </button>

            <div
                v-if="t.timeout"
                :key="t.version"
                class="toast__progress"
                :class="{
                    'toast__progress--hidden': t.hideProgressBar,
                    'toast__progress--paused': isPaused(t),
                }"
                :style="{ animationDuration: `${t.timeout}ms` }"
                @animationend="toast.dismiss(t.id)"
            />
        </div>
    </TransitionGroup>
</template>

<style scoped>
.toast-stack {
    position: fixed;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 22rem;
    max-width: calc(100% - 2rem);
    pointer-events: none;
}

.toast-stack--top-left,
.toast-stack--top-center,
.toast-stack--top-right {
    top: 1rem;
}

.toast-stack--bottom-left,
.toast-stack--bottom-center,
.toast-stack--bottom-right {
    bottom: 1rem;
}

.toast-stack--top-left,
.toast-stack--bottom-left {
    left: 1rem;
    --toast-offset: translateX(-1rem);
}

.toast-stack--top-right,
.toast-stack--bottom-right {
    right: 1rem;
    --toast-offset: translateX(1rem);
}

.toast-stack--top-center,
.toast-stack--bottom-center {
    left: 50%;
    transform: translateX(-50%);
}

.toast-stack--top-center {
    --toast-offset: translateY(-1rem);
}

.toast-stack--bottom-center {
    --toast-offset: translateY(1rem);
}

.toast {
    --toast-tone: var(--v-theme-text-secondary, 71, 84, 103);
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding: 0.75rem 0.75rem 0.75rem 0.875rem;
    overflow: hidden;
    pointer-events: auto;
    color: rgb(var(--v-theme-on-surface));
    background: rgb(var(--v-theme-surface));
    border: 0.0625rem solid rgb(var(--v-theme-outline, 225, 228, 232));
    border-radius: 0.75rem;
}

.toast--success {
    --toast-tone: var(--v-theme-success, 76, 175, 80);
}

.toast--error {
    --toast-tone: var(--v-theme-error, 176, 0, 32);
}

.toast--warning {
    --toast-tone: var(--v-theme-warning, 251, 140, 0);
}

.toast--info {
    --toast-tone: var(--v-theme-primary, 25, 118, 210);
}

.toast--clickable {
    cursor: pointer;
}

.toast__icon {
    flex-shrink: 0;
    margin-top: 0.0625rem;
    color: rgb(var(--toast-tone));
}

.toast__body {
    flex: 1;
    min-width: 0;
    font-size: 0.8125rem;
    font-weight: 600;
    line-height: 1.25rem;
    word-break: break-word;
}

.toast__close {
    position: relative;
    display: inline-flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    margin: -0.125rem -0.125rem 0 0;
    padding: 0;
    color: rgb(var(--v-theme-text-disabled, 148, 157, 173));
    cursor: pointer;
    background: transparent;
    border: none;
    border-radius: 0.5rem;
    outline: none;
    transition: color 0.15s ease;
    user-select: none;
    -webkit-user-select: none;
}

.toast__close:hover {
    color: rgb(var(--v-theme-on-surface));
}

.toast__close:focus-visible {
    box-shadow: 0 0 0 0.1875rem rgba(var(--v-theme-primary), 0.15);
}

.toast__progress {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 0.125rem;
    background: rgb(var(--toast-tone));
    border-radius: 0.125rem;
    opacity: 0.6;
    transform-origin: left center;
    animation-name: toast-progress;
    animation-timing-function: linear;
    animation-fill-mode: forwards;
}

.toast__progress--paused {
    animation-play-state: paused;
}

.toast__progress--hidden {
    visibility: hidden;
}

@keyframes toast-progress {
    from {
        transform: scaleX(1);
    }
    to {
        transform: scaleX(0);
    }
}

.toast-enter-active,
.toast-leave-active,
.toast-move {
    transition:
        opacity 0.18s ease,
        transform 0.18s ease;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
    transform: var(--toast-offset);
}

.toast-leave-active {
    position: absolute;
    width: 100%;
}
</style>
