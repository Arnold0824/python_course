import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "highlight.js/styles/github-dark.css";
import "./assets/lesson-theme.css";
import "./assets/chapter-two-extra.css";

createApp(App).use(router).mount("#app");
