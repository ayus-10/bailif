import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const lightColors = {
    primary: "#1976d2",
    "primary-darken-1": "#1565c0",
    secondary: "#48a9a6",
    "secondary-darken-1": "#018786",

    error: "#b00020",
    info: "#2196f3",
    success: "#4caf50",
    warning: "#fb8c00",

    background: "#ffffff",
    surface: "#ffffff",
    "surface-bright": "#ffffff",
    "surface-light": "#eeeeee",
    "surface-variant": "#f8f9fa",
    "on-surface-variant": "#eeeeee",

    "on-background": "#1a1f2c",
    "on-surface": "#1a1f2c",
    "on-primary": "#ffffff",
    "on-secondary": "#ffffff",
    "on-error": "#ffffff",
    "on-info": "#ffffff",
    "on-success": "#ffffff",
    "on-warning": "#ffffff",

    outline: "#e1e4e8",
    "outline-variant": "#a5acb6",
};

const darkColors = {
    primary: "#2196f3",
    "primary-darken-1": "#1976d2",
    secondary: "#54b6b3",
    "secondary-darken-1": "#48a9a6",

    error: "#cf6679",
    info: "#2196f3",
    success: "#4caf50",
    warning: "#fb8c00",

    background: "#121212",
    surface: "#212121",
    "surface-bright": "#2c2c2c",
    "surface-light": "#2c2c2c",
    "surface-variant": "#c7c7c7",
    "on-surface-variant": "#424242",

    "on-background": "#e5e7eb",
    "on-surface": "#e5e7eb",
    "on-primary": "#000000",
    "on-secondary": "#000000",
    "on-error": "#000000",
    "on-info": "#000000",
    "on-success": "#000000",
    "on-warning": "#000000",

    outline: "#3a3f4b",
    "outline-variant": "#565d6b",
};

/**
 * Configured Vuetify instance, registered as a Vue plugin in main.js.
 * @see https://vuetifyjs.com/en/features/global-configuration/
 * @see https://vuetifyjs.com/en/styles/colors/ — full token reference
 */
const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: "light",
        themes: {
            light: { dark: false, colors: lightColors },
            dark: { dark: true, colors: darkColors },
        },
    },
});

export default vuetify;
