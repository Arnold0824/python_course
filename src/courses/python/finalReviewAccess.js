export const FINAL_REVIEW_STUDENT_IDS_PATH = "/courses/python/final/学号.txt";
export const FINAL_REVIEW_PDF_PATH = "/courses/python/final/Python编程与科学计算复习资料.pdf";
export const FINAL_REVIEW_PDF_DOWNLOAD_NAME = "Python编程与科学计算复习资料.pdf";

export function normalizeStudentId(value) {
  return String(value || "").replace(/\D/g, "");
}

export function parseAllowedStudentIds(text) {
  return new Set(
    String(text || "")
      .split(/[\s,，;；]+/)
      .map((item) => normalizeStudentId(item))
      .filter(Boolean)
  );
}

export function validateStudentId(value, allowedIds) {
  const studentId = normalizeStudentId(value);

  if (!studentId) {
    return {
      ok: false,
      studentId,
      message: "请输入学号。",
    };
  }

  if (!allowedIds?.has(studentId)) {
    return {
      ok: false,
      studentId,
      message: "未在本课程名单中找到该学号，请检查是否输入正确。",
    };
  }

  return {
    ok: true,
    studentId,
    message: "验证通过，可以下载复习资料。",
  };
}
