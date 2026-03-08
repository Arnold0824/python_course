import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { installPageViewTracking } from "./services/analytics";
import "highlight.js/styles/github-dark.css";
import "./assets/lesson-theme.css";
import "./assets/chapter-two-extra.css";

installPageViewTracking(router);

createApp(App).use(router).mount("#app");
