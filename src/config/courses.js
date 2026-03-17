import { pythonCourse } from "../courses/python/course";
import { carlaCourse } from "../courses/carla/course";

export const courses = [pythonCourse, carlaCourse];

export function getCourseById(courseId) {
  return courses.find((course) => course.id === String(courseId)) || null;
}

export function getCourseHome(courseId) {
  return getCourseById(courseId)?.home || courses[0]?.home || "/";
}
