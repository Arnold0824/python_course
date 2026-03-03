export const courseChapters = [
  { no: "01", id: "1", label: "第一章 认识 Python", path: "/chapter/1" },
  { no: "02", id: "2", label: "第二章 基本语法与知识", path: "/chapter/2" },
];

export function toChapterPath(id) {
  const hit = courseChapters.find((chapter) => chapter.id === String(id));
  return hit ? hit.path : "/chapter/1";
}
