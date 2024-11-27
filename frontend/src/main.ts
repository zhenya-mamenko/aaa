import { registerPlugins } from "@/plugins";
import { createApp } from "vue";

import App from "./App.vue";
import { setLocale } from "./common/locale";

const app = createApp(App)

registerPlugins(app)

setLocale("ru")

app.mount("#app")
