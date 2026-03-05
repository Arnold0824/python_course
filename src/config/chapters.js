export const courseChapters = [
  { no: "01", id: "1", label: "第一章 认识 Python", path: "/chapter/1" },
  { no: "02", id: "2", label: "第二章 基础语法与数据类型", path: "/chapter/2" },
  { no: "03", id: "3", label: "第三章 运算符与控制流程", path: "/chapter/3" },
];

export function toChapterPath(id) {
  const hit = courseChapters.find((chapter) => chapter.id === String(id));
  return hit ? hit.path : "/chapter/1";
}
