import { createRouter, createWebHashHistory } from "vue-router";
import ChapterOneView from "../views/ChapterOneView.vue";
import ChapterTwoView from "../views/ChapterTwoView.vue";
import ChapterThreeView from "../views/ChapterThreeView.vue";

const routes = [
  {
    path: "/",
    redirect: "/chapter/1",
  },
  {
    path: "/chapter/1",
    name: "chapter-1",
    component: ChapterOneView,
    meta: { chapterId: "1" },
  },
  {
    path: "/chapter/2",
    name: "chapter-2",
    component: ChapterTwoView,
    meta: { chapterId: "2" },
  },
  {
    path: "/chapter/3",
    name: "chapter-3",
    component: ChapterThreeView,
    meta: { chapterId: "3" },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/chapter/1",
  },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
