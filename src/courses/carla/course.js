export const carlaCourse = {
  id: "carla",
  label: "Carla自动驾驶仿真",
  shortLabel: "Carla自动驾驶仿真",
  home: "/carla/chapter/1",
  chapters: [
    {
      no: "01",
      id: "1",
      label: "第一章 环境搭建、运行机制与首次连接",
      path: "/carla/chapter/1",
      component: () => import("./views/Chapter01View.vue"),
    },
    {
      no: "02",
      id: "2",
      label: "第二章 车辆生成、传感器挂载与自动采图",
      path: "/carla/chapter/2",
      component: () => import("./views/Chapter03View.vue"),
    },
    {
      no: "03",
      id: "3",
      label: "第三章 RGB与语义分割双通道采集对齐",
      path: "/carla/chapter/3",
      component: () => import("./views/Chapter04View.vue"),
    },
  ],
};
