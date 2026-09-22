import { onBeforeUnmount, onMounted, ref } from "vue";

export function useWindowBlurred() {
    const blurred = ref(false);

    const onBlur = () => (blurred.value = true);
    const onFocus = () => (blurred.value = false);

    onMounted(() => {
        window.addEventListener("blur", onBlur);
        window.addEventListener("focus", onFocus);
    });

    onBeforeUnmount(() => {
        window.removeEventListener("blur", onBlur);
        window.removeEventListener("focus", onFocus);
    });

    return blurred;
}
