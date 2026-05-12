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
      component: () => import("./views/Chapter02View.vue"),
    },
    {
      no: "03",
      id: "3",
      label: "第三章 RGB与语义分割双通道采集对齐",
      path: "/carla/chapter/3",
      component: () => import("./views/Chapter03View.vue"),
    },
    {
      no: "04",
      id: "4",
      label: "第四章 自动驾驶参数对比与统计分析",
      path: "/carla/chapter/4",
      component: () => import("./views/Chapter04View.vue"),
    },
    {
      no: "05",
      id: "5",
      label: "第五章 红灯状态监测与事件日志分析",
      path: "/carla/chapter/5",
      component: () => import("./views/Chapter05View.vue"),
    },
  ],
};
