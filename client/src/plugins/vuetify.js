import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

/**
 * Configured Vuetify instance, registered as a Vue plugin in main.js.
 * @see https://vuetifyjs.com/en/features/global-configuration/
 */
const vuetify = createVuetify({
  components,
  directives,
})

export default vuetify
