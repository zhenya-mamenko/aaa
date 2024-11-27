/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { md3 } from "vuetify/blueprints";
import { en, ru } from "vuetify/locale";


// Composables
import { createVuetify, type ThemeDefinition } from "vuetify";


const lightTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: "#FFFFFF",
    borderColor: "#263238",
    surface: "#FFFFFF",
    "surface-light": "#ECEFF1",
    primary: "#607D8B",
    "primary-darken-1": "#546E7A",
    "primary-darken-3": "#37474F",
    "primary-lighten-5": "#ECEFF1",
    secondary: "#424242",
    "secondary-darken-1": "#212121",
    error: "#B00020",
    info: "#2196F3",
    success: "#4CAF50",
    warning: "#FB8C00",
  },
}


export default createVuetify({
  blueprint: md3,
  defaults: {
    global: {
      ripple: false,
    },
    VTextField: {
      baseColor: "primary",
      bgColor: "surface",
    },
  },
  locale: {
    locale: "en",
    fallback: "en",
    messages: {
      en, ru,
    },
  },
  theme: {
    defaultTheme: "lightTheme",
    themes: {
      lightTheme,
    },
  },
})
