import { createRouter, createWebHashHistory } from "vue-router";
import { courses } from "../config/courses";
import AdminStatsView from "../views/AdminStatsView.vue";

const lessonRoutes = courses.flatMap((course) =>
  course.chapters.map((chapter) => ({
    path: chapter.path,
    name: `${course.id}-chapter-${chapter.id}`,
    component: chapter.component,
    meta: {
      courseId: course.id,
      chapterId: chapter.id,
    },
  }))
);

const routes = [
  {
    path: "/",
    redirect: "/python/chapter/1",
  },
  {
    path: "/chapter/:chapterId",
    redirect: (to) => `/python/chapter/${to.params.chapterId}`,
  },
  {
    path: "/python",
    redirect: "/python/chapter/1",
  },
  {
    path: "/carla",
    redirect: "/carla/chapter/1",
  },
  ...lessonRoutes,
  {
    path: "/admin/stats",
    name: "admin-stats",
    component: AdminStatsView,
    meta: { hideChapterNav: true },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/python/chapter/1",
  },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
