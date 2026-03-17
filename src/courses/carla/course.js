export const carlaCourse = {
  id: "carla",
  label: "Carla自动驾驶仿真",
  shortLabel: "Carla自动驾驶仿真",
  home: "/carla/chapter/1",
  chapters: [
    {
      no: "01",
      id: "1",
      label: "第一章 认识CARLA与基础使用",
      path: "/carla/chapter/1",
      component: () => import("./views/Chapter01View.vue"),
    },
  ],
};
