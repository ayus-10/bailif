import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

/**
 * Configured Vuetify instance, registered as a Vue plugin in main.js.
 * @see https://vuetifyjs.com/en/features/global-configuration/
 * @see https://vuetifyjs.com/en/styles/colors/
 */
const vuetify = createVuetify({
    components,
    directives,

    theme: {
        defaultTheme: "light",

        themes: {
            light: {
                dark: false,
            },
            dark: {
                dark: true,
            },
        },
    },
});

export default vuetify;
